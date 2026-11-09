"""
Proyecto: Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Componente Práctico - Fase 4: Prácticas Simuladas
Curso: Programación (213023) - UNAD
"""

import os
import sys

# Asegurar que la ruta base sea el directorio del script
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_ACTUAL not in sys.path:
    sys.path.insert(0, DIRECTORIO_ACTUAL)
os.chdir(DIRECTORIO_ACTUAL)

from src.entidades import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.reservas import Reserva
from src.excepciones import (
    ErrorSoftwareFJ,
    ErrorDatoInvalido,
    ErrorServicioNoDisponible,
    ErrorReservaInvalida
)
from src.logger import registrar_evento, registrar_error


def ejecutar_operacion(numero_op: int, descripcion: str, accion_lambda):
    """
    Función envoltorio para ejecutar operaciones simuladas aplicando
    la estructura try / except / else / finally y trazabilidad en logs.
    """
    print(f"\n========================================================")
    print(f"OPERACIÓN #{numero_op}: {descripcion}")
    print(f"========================================================")
    resultado = None
    try:
        resultado = accion_lambda()
    except (ErrorDatoInvalido, ErrorServicioNoDisponible, ErrorReservaInvalida) as ex:
        print(f"[EXCEPCIÓN CONTROLADA] {type(ex).__name__}: {ex}")
        registrar_error(f"Falla de negocio controlada en Operación #{numero_op}", ex)
    except Exception as ex_inesperada:
        print(f"[ERROR INESPERADO] {type(ex_inesperada).__name__}: {ex_inesperada}")
        registrar_error(f"Error inesperado en Operación #{numero_op}", ex_inesperada)
    else:
        print(f"[ÉXITO] Operación procesada satisfactoriamente.")
        if resultado:
            print(f"Detalle: {resultado}")
    finally:
        print(f"[AUDITORÍA] Ciclo de Operación #{numero_op} finalizado. Registro guardado en app.log.")
    return resultado


def ejecutar_simulacion_10_operaciones():
    """Ejecuta secuencialmente las 10 operaciones de prueba requeridas por la guía."""
    print("=" * 65)
    print("      SOFTWARE FJ - SISTEMA DE GESTIÓN DE CLIENTES Y SERVICIOS")
    print("             COMPONENTE PRÁCTICO - FASE 4 (SIMULACIÓN)")
    print("=" * 65)

    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # 1. Registro Válido de Cliente
    def op1():
        c = Cliente("1018456789", "Carlos Gomez", "carlos.gomez@correo.com", "3105551234")
        lista_clientes.append(c)
        return c.obtener_resumen()
    ejecutar_operacion(1, "Registro VÁLIDO de un nuevo cliente", op1)

    # 2. Registro Inválido de Cliente (Formato de correo incorrecto)
    def op2():
        c_invalido = Cliente("1020304050", "Mariana Ruiz", "correo_sin_arroba.com", "3001234567")
        lista_clientes.append(c_invalido)
        return c_invalido.obtener_resumen()
    ejecutar_operacion(2, "Registro INVÁLIDO de cliente (Correo sin formato válido)", op2)

    # 3. Registro Inválido de Cliente (Nombre con dígitos)
    def op3():
        c_invalido = Cliente("1098765432", "Andres Felipe 123", "andres@correo.com", "3209876543")
        lista_clientes.append(c_invalido)
        return c_invalido.obtener_resumen()
    ejecutar_operacion(3, "Registro INVÁLIDO de cliente (Nombre con números)", op3)

    # 4. Creación Válida de Servicios (Categorías exactas del Anexo 3)
    def op4():
        s1 = ReservaSala("SAL-01", "Reserva de Sala de Conferencias", 80000.0, capacidad_maxima=25)
        s2 = AlquilerEquipo("EQP-01", "Alquiler de Equipo de Computo", 50000.0, stock_disponible=5)
        s3 = AsesoriaEspecializada("ASE-01", "Asesoria Especializada en Software", 120000.0, especialista="Consultor Senior")
        lista_servicios.extend([s1, s2, s3])
        return f"Servicios cargados: {len(lista_servicios)} items activos."
    ejecutar_operacion(4, "Creación VÁLIDA de los 3 servicios del Anexo 3", op4)

    # 5. Creación Inválida de Servicio (Tarifa negativa o cero)
    def op5():
        s_erroneo = ReservaSala("SAL-ERR", "Reserva de Sala Invalida", -40000.0, capacidad_maxima=10)
        lista_servicios.append(s_erroneo)
        return s_erroneo.obtener_resumen()
    ejecutar_operacion(5, "Creación INVÁLIDA de servicio (Tarifa negativa)", op5)

    # 6. Reserva Válida y Confirmación
    def op6():
        cliente = lista_clientes[0]
        sala = lista_servicios[0]
        reserva = Reserva("RES-1001", cliente, sala, unidades=4)
        reserva.procesar_reserva(descuento=0.10, impuesto=0.19)
        reserva.confirmar()
        lista_reservas.append(reserva)
        return reserva.obtener_detalle()
    ejecutar_operacion(6, "Creación, cálculo y confirmación VÁLIDA de reserva (Reserva de Sala)", op6)

    # 7. Reserva Fallida por Capacidad/Aforo Excedido
    def op7():
        cliente = lista_clientes[0]
        sala = lista_servicios[0]
        reserva = Reserva("RES-1002", cliente, sala, unidades=40)
        reserva.procesar_reserva()
        return reserva.obtener_detalle()
    ejecutar_operacion(7, "Reserva FALLIDA por exceder capacidad máxima de la sala", op7)

    # 8. Reserva Fallida por Stock Insuficiente
    def op8():
        cliente = lista_clientes[0]
        equipo = lista_servicios[1]
        reserva = Reserva("RES-1003", cliente, equipo, unidades=10)
        reserva.procesar_reserva()
        return reserva.obtener_detalle()
    ejecutar_operacion(8, "Reserva FALLIDA por stock insuficiente en alquiler de equipos", op8)

    # 9. Operación Inválida en Ciclo de Vida (Confirmar sin liquidar)
    def op9():
        cliente = lista_clientes[0]
        asesoria = lista_servicios[2]
        reserva = Reserva("RES-1004", cliente, asesoria, unidades=2)
        reserva.confirmar()
        return reserva.obtener_detalle()
    ejecutar_operacion(9, "Violación de flujo: Confirmar reserva sin haberla liquidado", op9)

    # 10. Cancelación Exitosa y Reintento Inválido
    def op10():
        reserva_valida = lista_reservas[0]
        reserva_valida.cancelar("Cliente solicitó cancelación formal de la reserva.")
        print(f"-> Estado intermedio: {reserva_valida.estado}")
        reserva_valida.cancelar("Segundo intento indebido de cancelación.")
        return reserva_valida.obtener_detalle()
    ejecutar_operacion(10, "Cancelación de reserva y validación ante doble cancelación", op10)

    print("\n" + "=" * 65)
    print("Simulación de 10 operaciones finalizada con éxito.")
    print("=" * 65)


def menu_interactivo():
    """Menú por consola interactivo adaptable al Anexo 3."""
    clientes = [
        Cliente("1018456789", "Carlos Gomez", "carlos.gomez@correo.com", "3105551234")
    ]
    servicios = [
        ReservaSala("SAL-01", "Reserva de Sala de Conferencias", 80000.0, capacidad_maxima=25),
        AlquilerEquipo("EQP-01", "Alquiler de Equipo de Computo", 50000.0, stock_disponible=5),
        AsesoriaEspecializada("ASE-01", "Asesoria Especializada en Software", 120000.0, especialista="Consultor Senior")
    ]
    reservas = []

    while True:
        print("\n" + "=".center(55, "="))
        print("          SOFTWARE FJ - SISTEMA DE GESTIÓN")
        print("                 CONSOLA INTERACTIVA")
        print("=".center(55, "="))
        print("1. Registrar nuevo Cliente")
        print("2. Listar Clientes y Catálogo de Servicios")
        print("3. Crear y Procesar Reserva")
        print("4. Confirmar Reserva")
        print("5. Cancelar Reserva")
        print("6. Consultar Historial de Reservas")
        print("7. Re-ejecutar simulación de 10 operaciones")
        print("8. Salir de la aplicación")
        print("-" * 55)

        opcion = input("Seleccione una opción (1-8): ").strip()

        if opcion == "1":
            try:
                print("\n--- REGISTRAR NUEVO CLIENTE ---")
                cedula = input("Documento / Cédula: ").strip()
                nombre = input("Nombre completo: ").strip()
                correo = input("Correo electrónico: ").strip()
                telefono = input("Teléfono de contacto: ").strip()

                nuevo = Cliente(cedula, nombre, correo, telefono)
                clientes.append(nuevo)
                print(f"\n[OK] {nuevo.obtener_resumen()}")
            except ErrorDatoInvalido as ex:
                print(f"\n[ERROR CONTROLADO] {ex}")
                registrar_error("Falla al registrar cliente desde consola", ex)

        elif opcion == "2":
            print("\n--- CLIENTES REGISTRADOS ---")
            if not clientes:
                print("(No hay clientes registrados en memoria)")
            for i, c in enumerate(clientes):
                print(f" [{i}] {c.obtener_resumen()}")

            print("\n--- CATÁLOGO DE SERVICIOS (ANEXO 3) ---")
            for i, s in enumerate(servicios):
                print(f" [{i}] {s.obtener_resumen()}")

        elif opcion == "3":
            try:
                if not clientes:
                    print("\n[AVISO] Debe registrar al menos un cliente en la opción 1.")
                    continue

                print("\n--- CREAR Y PROCESAR RESERVA ---")
                cod = input("Código de reserva (ej. RES-2001): ").strip()

                print("\nSeleccione el Cliente:")
                for i, c in enumerate(clientes):
                    print(f"  [{i}] {c.nombre} (ID: {c.cedula})")
                idx_c = int(input("Número de cliente: "))
                cliente_sel = clientes[idx_c]

                print("\nSeleccione el Servicio ofertado:")
                for i, s in enumerate(servicios):
                    print(f"  [{i}] {s.nombre}")
                idx_s = int(input("Número de servicio: "))
                servicio_sel = servicios[idx_s]

                if isinstance(servicio_sel, ReservaSala):
                    prompt_unidades = "Ingrese la duración en HORAS de la sala: "
                elif isinstance(servicio_sel, AlquilerEquipo):
                    prompt_unidades = "Ingrese la cantidad de EQUIPOS a alquilar: "
                elif isinstance(servicio_sel, AsesoriaEspecializada):
                    prompt_unidades = "Ingrese la cantidad de SESIONES de asesoría: "
                else:
                    prompt_unidades = "Ingrese las unidades solicitadas: "

                cant = int(input(prompt_unidades))

                nueva_reserva = Reserva(cod, cliente_sel, servicio_sel, cant)
                total = nueva_reserva.procesar_reserva(descuento=0.05, impuesto=0.19)
                reservas.append(nueva_reserva)
                print(f"\n[OK] Reserva procesada satisfactoriamente.")
                print(f"Detalle: {nueva_reserva.obtener_detalle()}")

            except (ValueError, IndexError):
                print("\n[ERROR] Debe seleccionar un índice numérico válido de la lista.")
            except (ErrorDatoInvalido, ErrorServicioNoDisponible, ErrorReservaInvalida) as ex:
                print(f"\n[EXCEPCIÓN CONTROLADA] {type(ex).__name__}: {ex}")
                registrar_error("Error al procesar reserva interactiva", ex)

        elif opcion == "4":
            try:
                if not reservas:
                    print("\n[AVISO] No hay reservas disponibles para confirmar.")
                    continue

                print("\n--- CONFIRMAR RESERVA ---")
                for i, r in enumerate(reservas):
                    print(f"  [{i}] {r.obtener_detalle()}")
                idx_r = int(input("Seleccione el número de reserva a confirmar: "))
                reservas[idx_r].confirmar()
                print(f"\n[OK] Reserva #{reservas[idx_r].codigo_reserva} confirmada exitosamente.")
            except (ValueError, IndexError):
                print("\n[ERROR] Selección inválida.")
            except ErrorReservaInvalida as ex:
                print(f"\n[EXCEPCIÓN CONTROLADA] {ex}")

        elif opcion == "5":
            try:
                if not reservas:
                    print("\n[AVISO] No hay reservas en el sistema.")
                    continue

                print("\n--- CANCELAR RESERVA ---")
                for i, r in enumerate(reservas):
                    print(f"  [{i}] {r.obtener_detalle()}")
                idx_r = int(input("Seleccione el número de reserva a cancelar: "))
                motivo = input("Motivo de cancelación: ").strip()
                reservas[idx_r].cancelar(motivo)
                print(f"\n[OK] Reserva #{reservas[idx_r].codigo_reserva} cancelada.")
            except (ValueError, IndexError):
                print("\n[ERROR] Selección no válida.")
            except ErrorReservaInvalida as ex:
                print(f"\n[EXCEPCIÓN CONTROLADA] {ex}")

        elif opcion == "6":
            print("\n--- HISTORIAL GENERAL DE RESERVAS ---")
            if not reservas:
                print("(No se han registrado reservas aún)")
            for r in reservas:
                print(f" - {r.obtener_detalle()}")

        elif opcion == "7":
            ejecutar_simulacion_10_operaciones()

        elif opcion == "8":
            print("\nCerrando aplicación Software FJ. Auditoría completa en 'logs/app.log'.")
            break

        else:
            print("\n[AVISO] Opción inválida. Seleccione un número entre 1 y 8.")


if __name__ == "__main__":
    try:
        # 1. Ejecución secuencial de la simulación exigida
        ejecutar_simulacion_10_operaciones()

        # 2. Apertura del menú interactivo por consola
        menu_interactivo()

    except Exception as error_fatal:
        print(f"\n[ERROR CRÍTICO] Fallo general del sistema: {error_fatal}")
    finally:
        # 3. Mantiene la consola abierta ante ejecuciones por doble clic
        input("\nPresione ENTER para salir de la ventana...")
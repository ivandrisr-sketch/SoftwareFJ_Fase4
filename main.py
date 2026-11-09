"""
Proyecto: Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Componente Práctico - Fase 4: Prácticas Simuladas
Curso: Programación (213023) - UNAD

Servicios definidos en el Anexo 3:
1. Reserva de Salas (ReservaSala)
2. Alquiler de Equipos (AlquilerEquipo)
3. Asesorías Especializadas (AsesoriaEspecializada)
"""

import os
import sys

# Asegurar que el directorio actual del script sea la raíz para importar 'src'
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

    # 4. Creación Válida de Servicios (Según las 3 categorías exactas del Anexo 3)
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
    """Menú por consola adaptado estrictamente a los requerimientos del Anexo 3."""
    clientes = [
        Cliente("1018456789", "Carlos Gomez", "carlos.gomez@correo.com", "31055
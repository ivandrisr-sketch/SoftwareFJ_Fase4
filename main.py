"""
Script Principal - Software FJ
Simulación de las 10 operaciones requeridas por la Fase 4.
Demuestra robustez, persistencia en memoria y manejo avanzado de excepciones.
"""
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


def main():
    print("=" * 65)
    print("      SOFTWARE FJ - SISTEMA DE GESTIÓN DE CLIENTES Y SERVICIOS")
    print("             COMPONENTE PRÁCTICO - FASE 4 (SIMULACIÓN)")
    print("=" * 65)

    # Contenedores en memoria (sin bases de datos)
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # ---------------------------------------------------------
    # OPERACIÓN 1: Registro Válido de Cliente
    # ---------------------------------------------------------
    def op1():
        c = Cliente("1018456789", "Carlos Gomez", "carlos.gomez@empresa.com", "3105551234")
        lista_clientes.append(c)
        return c.obtener_resumen()

    ejecutar_operacion(1, "Registro VÁLIDO de un nuevo cliente", op1)

    # ---------------------------------------------------------
    # OPERACIÓN 2: Registro Inválido de Cliente (Formato de correo incorrecto)
    # ---------------------------------------------------------
    def op2():
        # Provoca ErrorDatoInvalido por correo mal estructurado
        c_invalido = Cliente("1020304050", "Mariana Ruiz", "correo_sin_arroba.com", "3001234567")
        lista_clientes.append(c_invalido)
        return c_invalido.obtener_resumen()

    ejecutar_operacion(2, "Registro INVÁLIDO de cliente (Correo sin formato RFC/válido)", op2)

    # ---------------------------------------------------------
    # OPERACIÓN 3: Registro Inválido de Cliente (Nombre con números)
    # ---------------------------------------------------------
    def op3():
        # Provoca ErrorDatoInvalido por dígitos en el nombre
        c_invalido = Cliente("1098765432", "Andres Felipe 123", "andres@correo.com", "3209876543")
        lista_clientes.append(c_invalido)
        return c_invalido.obtener_resumen()

    ejecutar_operacion(3, "Registro INVÁLIDO de cliente (Nombre con números)", op3)

    # ---------------------------------------------------------
    # OPERACIÓN 4: Creación Válida de Catálogo de Servicios
    # ---------------------------------------------------------
    def op4():
        s1 = ReservaSala("SALA-01", "Sala de Capacitación Principal", 85000.0, capacidad_maxima=25)
        s2 = AlquilerEquipo("EQUIP-01", "Switch Allied Telesis 28 Puertos", 120000.0, stock_disponible=3)
        s3 = AsesoriaEspecializada("ASES-01", "Consultoría Arquitectura TI", 150000.0, especialista="Ing. Salcedo")
        lista_servicios.extend([s1, s2, s3])
        return f"Servicios cargados: {len(lista_servicios)} items activos."

    ejecutar_operacion(4, "Creación VÁLIDA de servicios en el catálogo", op4)

    # ---------------------------------------------------------
    # OPERACIÓN 5: Creación Inválida de Servicio (Tarifa negativa o cero)
    # ---------------------------------------------------------
    def op5():
        # Provoca ErrorDatoInvalido por costo inválido
        s_erroneo = ReservaSala("SALA-ERR", "Sala Vip Invalida", -50000.0, capacidad_maxima=10)
        lista_servicios.append(s_erroneo)
        return s_erroneo.obtener_resumen()

    ejecutar_operacion(5, "Creación INVÁLIDA de servicio (Tarifa negativa)", op5)

    # ---------------------------------------------------------
    # OPERACIÓN 6: Reserva Válida y Confirmación Completa
    # ---------------------------------------------------------
    def op6():
        cliente = lista_clientes[0]
        sala = lista_servicios[0]
        reserva = Reserva("RES-1001", cliente, sala, unidades=4) # 4 horas
        costo = reserva.procesar_reserva(descuento=0.10, impuesto=0.19)
        reserva.confirmar()
        lista_reservas.append(reserva)
        return reserva.obtener_detalle()

    ejecutar_operacion(6, "Creación, cálculo y confirmación VÁLIDA de reserva (Sala)", op6)

    # ---------------------------------------------------------
    # OPERACIÓN 7: Reserva Fallida por Capacidad/Aforo Excedido
    # ---------------------------------------------------------
    def op7():
        cliente = lista_clientes[0]
        sala = lista_servicios[0] # Capacidad máxima: 25 personas
        reserva = Reserva("RES-1002", cliente, sala, unidades=40) # Intenta reservar para 40 asistentes
        costo = reserva.procesar_reserva()
        return reserva.obtener_detalle()

    ejecutar_operacion(7, "Reserva FALLIDA por exceder capacidad de aforo de sala", op7)

    # ---------------------------------------------------------
    # OPERACIÓN 8: Reserva Fallida por Stock de Equipos Insuficiente
    # ---------------------------------------------------------
    def op8():
        cliente = lista_clientes[0]
        equipo = lista_servicios[1] # Stock disponible: 3 unidades
        reserva = Reserva("RES-1003", cliente, equipo, unidades=10) # Solicita 10 unidades
        costo = reserva.procesar_reserva()
        return reserva.obtener_detalle()

    ejecutar_operacion(8, "Reserva FALLIDA de alquiler por falta de stock de equipo", op8)

    # ---------------------------------------------------------
    # OPERACIÓN 9: Operación Inválida en Ciclo de Vida (Confirmar sin procesar)
    # ---------------------------------------------------------
    def op9():
        cliente = lista_clientes[0]
        asesoria = lista_servicios[2]
        reserva = Reserva("RES-1004", cliente, asesoria, unidades=2)
        # Se omite intencionalmente procesar_reserva(), lo que debe lanzar ErrorReservaInvalida
        reserva.confirmar()
        return reserva.obtener_detalle()

    ejecutar_operacion(9, "Violación de flujo: Confirmar reserva sin haberla liquidado", op9)

    # ---------------------------------------------------------
    # OPERACIÓN 10: Cancelación Exitosa y Reintento Inválido (Doble Cancelación)
    # ---------------------------------------------------------
    def op10():
        # Primero se cancela la reserva válida existente
        reserva_valida = lista_reservas[0]
        reserva_valida.cancelar("Cliente solicitó reprogramación por motivos de fuerza mayor.")
        print(f"-> Estado intermedio: {reserva_valida.estado}")
        
        # Ahora se fuerza un segundo intento sobre la misma reserva cancelada
        reserva_valida.cancelar("Segundo intento indebido de cancelación.")
        return reserva_valida.obtener_detalle()

    ejecutar_operacion(10, "Cancelación de reserva y validación de error ante doble cancelación", op10)

    print("\n" + "=" * 65)
    print("Simulación finalizada. Todas las excepciones fueron capturadas.")
    print("Revise el archivo 'logs/app.log' para comprobar la auditoría de eventos.")
    print("=" * 65)


if __name__ == "__main__":
    main()
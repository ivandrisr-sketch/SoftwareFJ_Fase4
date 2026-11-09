"""
Módulo de Gestión de Reservas para Software FJ.
Implementa el ciclo de vida de una reserva (creación, confirmación, cancelación)
y el cálculo totalizado sin recurrir a bases de datos.
"""
from datetime import datetime
from src.entidades import Cliente
from src.servicios import Servicio
from src.excepciones import ErrorDatoInvalido, ErrorReservaInvalida, ErrorServicioNoDisponible
from src.logger import registrar_evento, registrar_error


class Reserva:
    """Clase que representa una reserva vinculando cliente, servicio, duración y estado."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA")

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio: Servicio, unidades: int):
        if not codigo_reserva or not str(codigo_reserva).strip():
            raise ErrorDatoInvalido("El código de reserva no puede estar vacío.")
        if not isinstance(cliente, Cliente):
            raise ErrorDatoInvalido("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorDatoInvalido("La reserva requiere un objeto Servicio válido.")
        if unidades <= 0:
            raise ErrorDatoInvalido(f"Las unidades solicitadas ({unidades}) deben ser mayores a cero.")

        self._codigo_reserva = str(codigo_reserva).strip()
        self._cliente = cliente
        self._servicio = servicio
        self._unidades = unidades
        self._fecha_creacion = datetime.now()
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

        registrar_evento(
            f"Reserva creada [ID: {self._codigo_reserva}] para el cliente "
            f"{self._cliente.nombre} en estado PENDIENTE."
        )

    @property
    def codigo_reserva(self) -> str:
        return self._codigo_reserva

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def unidades(self) -> int:
        return self._unidades

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_reserva(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if self._estado == "CANCELADA":
            raise ErrorReservaInvalida(f"No se puede procesar la reserva '{self._codigo_reserva}' porque está cancelada.")

        self._servicio.verificar_disponibilidad(self._unidades)
        self._costo_total = self._servicio.calcular_costo(self._unidades, descuento, impuesto)
        registrar_evento(
            f"Reserva liquidada: {self._codigo_reserva} | Total calculado: ${self._costo_total:,.2f}"
        )
        return self._costo_total

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise ErrorReservaInvalida(
                f"Solo reservas en estado PENDIENTE pueden ser confirmadas. Estado actual: {self._estado}"
            )
        if self._costo_total <= 0:
            raise ErrorReservaInvalida(
                f"No se puede confirmar la reserva {self._codigo_reserva} sin haber procesado el costo previamente."
            )
        self._estado = "CONFIRMADA"
        registrar_evento(f"Reserva {self._codigo_reserva} confirmada exitosamente.")

    def cancelar(self, motivo: str):
        if self._estado == "CANCELADA":
            raise ErrorReservaInvalida(f"La reserva {self._codigo_reserva} ya se encuentra cancelada.")
        if self._estado == "COMPLETADA":
            raise ErrorReservaInvalida("Una reserva COMPLETADA no puede ser cancelada.")
        
        self._estado = "CANCELADA"
        registrar_evento(f"Reserva {self._codigo_reserva} CANCELADA. Motivo: {motivo}")

    def obtener_detalle(self) -> str:
        return (
            f"Reserva #{self._codigo_reserva} | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} (x{self._unidades}) | "
            f"Total: ${self._costo_total:,.2f}"
        )
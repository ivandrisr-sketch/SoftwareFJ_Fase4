"""
Módulo de Servicios de Software FJ.
Implementa la clase abstracta Servicio y las tres especializaciones:
- ReservaSala
- AlquilerEquipo
- AsesoriaEspecializada
"""
from abc import ABC, abstractmethod
from src.entidades import EntidadBase
from src.excepciones import ErrorDatoInvalido, ErrorServicioNoDisponible
from src.logger import registrar_evento


class Servicio(EntidadBase):
    """Clase abstracta base para todos los servicios ofertados."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        super().__init__(identificador=codigo)
        if tarifa_base <= 0:
            raise ErrorDatoInvalido(f"La tarifa base ({tarifa_base}) debe ser un monto mayor a cero.")
        self._nombre = nombre
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise ErrorDatoInvalido("El estado de disponibilidad debe ser booleano.")
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, unidades: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        pass

    @abstractmethod
    def verificar_disponibilidad(self, cantidad_solicitada: int) -> bool:
        pass


class ReservaSala(Servicio):
    """Servicio especializado: Reserva de salas de conferencias o cómputo."""

    def __init__(self, codigo: str, nombre: str, tarifa_por_hora: float, capacidad_maxima: int):
        super().__init__(codigo, nombre, tarifa_por_hora)
        if capacidad_maxima <= 0:
            raise ErrorDatoInvalido("La capacidad máxima de la sala debe ser superior a cero.")
        self._capacidad_maxima = capacidad_maxima

    def verificar_disponibilidad(self, asistentes: int) -> bool:
        if not self._disponible:
            raise ErrorServicioNoDisponible(f"La sala '{self.nombre}' no se encuentra activa para reservas.")
        if asistentes > self._capacidad_maxima:
            raise ErrorServicioNoDisponible(
                f"Aforo excedido: la sala '{self.nombre}' admite máximo {self._capacidad_maxima} personas "
                f"(solicitado: {asistentes})."
            )
        return True

    def calcular_costo(self, horas: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if horas <= 0:
            raise ErrorDatoInvalido("La duración en horas debe ser de al menos 1 hora.")
        subtotal = self._tarifa_base * horas
        monto_descuento = subtotal * descuento
        monto_con_descuento = subtotal - monto_descuento
        total = monto_con_descuento * (1 + impuesto)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Sala: {self.nombre} (ID: {self.identificador}) | Capacidad: {self._capacidad_maxima} pax | Tarifa/h: ${self._tarifa_base:,.2f}"


class AlquilerEquipo(Servicio):
    """Servicio especializado: Alquiler de hardware y dispositivos técnicos."""

    def __init__(self, codigo: str, nombre: str, tarifa_por_dia: float, stock_disponible: int):
        super().__init__(codigo, nombre, tarifa_por_dia)
        if stock_disponible < 0:
            raise ErrorDatoInvalido("El stock disponible no puede ser negativo.")
        self._stock_disponible = stock_disponible

    @property
    def stock(self) -> int:
        return self._stock_disponible

    def verificar_disponibilidad(self, cantidad_equipos: int) -> bool:
        if not self._disponible or self._stock_disponible <= 0:
            raise ErrorServicioNoDisponible(f"No hay unidades disponibles del equipo '{self.nombre}'.")
        if cantidad_equipos > self._stock_disponible:
            raise ErrorServicioNoDisponible(
                f"Stock insuficiente para '{self.nombre}': Solicitados {cantidad_equipos}, disponibles {self._stock_disponible}."
            )
        return True

    def calcular_costo(self, dias: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if dias <= 0:
            raise ErrorDatoInvalido("La cantidad de días de alquiler debe ser al menos 1.")
        costo_base = self._tarifa_base * dias
        seguro_tecnico = costo_base * 0.05
        subtotal = (costo_base - (costo_base * descuento)) + seguro_tecnico
        total = subtotal * (1 + impuesto)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Equipo: {self.nombre} (ID: {self.identificador}) | Stock: {self._stock_disponible} | Tarifa/día: ${self._tarifa_base:,.2f}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado: Consultoría y asesorías técnicas por sesión."""

    def __init__(self, codigo: str, nombre: str, tarifa_por_sesion: float, especialista: str):
        super().__init__(codigo, nombre, tarifa_por_sesion)
        if not especialista or not especialista.strip():
            raise ErrorDatoInvalido("Debe asignarse un especialista calificado a la asesoría.")
        self._especialista = especialista.strip()

    def verificar_disponibilidad(self, sesiones: int) -> bool:
        if not self._disponible:
            raise ErrorServicioNoDisponible(f"El consultor {self._especialista} no tiene agenda disponible.")
        if sesiones > 5:
            raise ErrorServicioNoDisponible("No es posible agendar más de 5 sesiones continuas de asesoría.")
        return True

    def calcular_costo(self, sesiones: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if sesiones <= 0:
            raise ErrorDatoInvalido("La cantidad de sesiones de asesoría debe ser superior a cero.")
        subtotal = self._tarifa_base * sesiones
        subtotal_con_descuento = subtotal - (subtotal * descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría: {self.nombre} (ID: {self.identificador}) | Experto: {self._especialista} | Tarifa/sesión: ${self._tarifa_base:,.2f}"
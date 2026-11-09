"""
Módulo de Excepciones Personalizadas para Software FJ.
Define la jerarquía de errores para controlar el flujo de la aplicación.
"""

class ErrorSoftwareFJ(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass

class ErrorDatoInvalido(ErrorSoftwareFJ):
    """Se lanza cuando un valor ingresado no cumple con el formato o rango esperado."""
    pass

class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio fuera de stock o sin cupo."""
    pass

class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza ante inconsistencias en el ciclo de vida de la reserva."""
    pass
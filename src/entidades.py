"""
Módulo de Entidades del Sistema Software FJ.
Implementa la clase abstracta EntidadBase y la clase Cliente.
"""
from abc import ABC, abstractmethod
import re
from src.excepciones import ErrorDatoInvalido
from src.logger import registrar_evento, registrar_error


class EntidadBase(ABC):
    """Clase abstracta que define la estructura común de las entidades del sistema."""

    def __init__(self, identificador: str):
        if not identificador or not str(identificador).strip():
            raise ErrorDatoInvalido("El identificador de la entidad no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self) -> str:
        """Obtiene el identificador único de la entidad."""
        return self._identificador

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para representar la entidad en formato de texto."""
        pass


class Cliente(EntidadBase):
    """Clase que representa un cliente con encapsulación y validación rigurosa."""

    def __init__(self, cedula: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador=cedula)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        registrar_evento(f"Cliente registrado exitosamente: {self._identificador} - {self._nombre}")

    @property
    def cedula(self) -> str:
        return self._identificador

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ErrorDatoInvalido("El nombre del cliente no puede ser un valor vacío.")
        if any(char.isdigit() for char in valor):
            raise ErrorDatoInvalido(f"El nombre '{valor}' no puede contener dígitos numéricos.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron_email, valor.strip()):
            raise ErrorDatoInvalido(f"El formato del correo '{valor}' es inválido.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise ErrorDatoInvalido(f"El teléfono '{valor}' debe ser numérico y tener al menos 7 dígitos.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        return f"Cliente [ID: {self._identificador}] {self._nombre} | Contacto: {self._correo} - Tel: {self._telefono}"
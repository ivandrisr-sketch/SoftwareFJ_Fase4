"""
Módulo de Registro de Eventos y Errores (Logs).
Permite auditar la ejecución de la aplicación sin recurrir a bases de datos.
"""
import logging
import os

# Asegurar que la carpeta de logs exista
os.makedirs("logs", exist_ok=True)
LOG_FILE = os.path.join("logs", "app.log")

# Configuración del logger centralizado
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")

def registrar_evento(mensaje: str):
    """Registra una operación exitosa o evento normal del sistema."""
    logger.info(mensaje)

def registrar_error(mensaje: str, excepcion: Exception = None):
    """Registra un error o excepción capturada en el archivo app.log."""
    if excepcion:
        logger.error(f"{mensaje} | Detalle técnico: {type(excepcion).__name__} - {str(excepcion)}")
    else:
        logger.error(mensaje)
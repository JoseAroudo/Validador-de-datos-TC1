import logging
import os
import traceback
from datetime import datetime

fecha = datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()

        # Para separadores visuales, escribir solo el mensaje sin prefijo de nivel.
        if message and (
            set(message.strip()) == {"="}
            or message.startswith(("❌ Fila", "⚠️ Fila"))
        ):
            return message

        return super().format(record)

class Logger():
    _logger = None

    @classmethod
    def _get_logger(cls):
        if cls._logger is not None:
            return cls._logger

        log_directory = 'Logs/'
        log_filename = fecha + '  validaciones.log'

        os.makedirs(log_directory, exist_ok=True)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = CustomFormatter(
            '%(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)

        cls._logger = logger
        return cls._logger
    
    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls._get_logger()
            log_method = {
                "critical": logger.critical,
                "debug": logger.debug,
                "error": logger.error,
                "info": logger.info,
                "warn": logger.warning,
                "warning": logger.warning,
            }.get(str(level).lower())

            if log_method is None:
                logger.warning(f"Nivel de log no soportado: {level}. Se registrara como info.")
                logger.info(message)
                return

            log_method(message)

        except Exception as ex:
            print(traceback.format_exc())#Esto es para traza de errores
            print(ex)
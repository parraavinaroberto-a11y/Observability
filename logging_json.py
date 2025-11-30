import logging
import logging.handlers
import json
import socket
import time
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "hostname": socket.gethostname(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

def get_logger(name="app", log_file="app.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        # Evitar handlers duplicados si se llama varias veces
        return logger

    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    # También a consola (útil para contenedores)
    console = logging.StreamHandler()
    console.setFormatter(JsonFormatter())
    logger.addHandler(console)

    return logger

if __name__ == "__main__":
    logger = get_logger()

    logger.info("Aplicación iniciada")
    try:
        for i in range(5):
            logger.info("Procesando petición", extra={"iteration": i})
            time.sleep(1)
        # Simular error
        1 / 0
    except Exception:
        logger.exception("Ocurrió un error inesperado")

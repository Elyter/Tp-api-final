import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler(
        "api.log",
        maxBytes=10000000,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger 
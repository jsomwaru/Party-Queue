import logging
import os

FORMAT = "%(asctime)s %(levelname)s %(name)s.%(funcName)s -- %(message)s"

DEBUG = os.environ.get("DEBUG")

def get_logger(name) -> logging.Logger:
    level = logging.INFO if not DEBUG else logging.DEBUG
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    logger.addHandler(ch)
    return logger

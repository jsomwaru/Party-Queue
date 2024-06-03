import logging
import os

FORMAT = "%(asctime)s %(levelname)s %(name)s.%(funcName)s -- %(message)s"

DEBUG = os.environ.get("DEBUG")


def get_logger(name) -> logging.Logger:
    level = logging.INFO if not DEBUG else logging.DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    app_log = logging.FileHandler("media/app.log")
    fmt = logging.Formatter(fmt=FORMAT)
    ch.setFormatter(fmt)
    ch.setLevel(level)
    logger.addHandler(ch)
    logger.addHandler(app_log)
    return logger

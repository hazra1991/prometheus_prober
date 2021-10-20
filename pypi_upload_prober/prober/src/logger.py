import logging
import sys
import os

from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from .errors import InvalidLoggingLevel

__all__ = ["get_logger"]


def get_console_handler():
    """outputs to console for debugging"""
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler


def get_file_error_handler(logger_name, log_dir, level, backup_cnt):
    """return a custom file  and  error file for logging """
    if not os.path.isdir(log_dir):
        raise NotADirectoryError()
    log_file = Path(log_dir) / f"{logger_name}.log"
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - fun:- %(funcName)s - %(message)s")
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=backup_cnt)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    err_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s")
    _err_file = log_file.parent / f'{logger_name}-ERROR.log'
    err_file_handler = TimedRotatingFileHandler(_err_file, when='midnight', backupCount=backup_cnt)
    err_file_handler.setLevel(logging.ERROR)
    err_file_handler.setFormatter(err_formatter)
    return file_handler, err_file_handler


def get_logger(logger_name, level, log_dir=None, backup_count=15):
    level = level.upper()
    levels = {"DEBUG": logging.DEBUG,
              "INFO": logging.INFO,
              "ERROR": logging.ERROR,
              "CRITICAL": logging.CRITICAL,
              "WARN": logging.WARN,
              "WARNING": logging.WARNING
              }
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if level not in levels:
        raise InvalidLoggingLevel(level)
    if log_dir:
        file_handler, err_handler = get_file_error_handler(logger_name, log_dir, levels[level], backup_count)
        logger.addHandler(file_handler)
        logger.addHandler(err_handler)
    else:
        logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger

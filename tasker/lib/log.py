# coding: utf-8

import sys
import logging


LEVEL_MAP = {
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
}


def get_log_level():
    return LEVEL_MAP.get('INFO')


def build_log_format():
    date_fmt = "%Y-%m-%d %H:%M:%S"
    fmt_string = '%(asctime)s  %(levelname)s  %(message)s'
    return logging.Formatter(fmt_string, date_fmt)


# Configure root logger used by requests/urlib
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(build_log_format())
consoleHandler.setLevel(get_log_level())
base_log = logging.getLogger('urllib3')
base_log.setLevel(get_log_level())
base_log.addHandler(consoleHandler)


class Log:
    def __init__(self, id):
        self._logger = logging.getLogger(id)
        if len(self._logger.handlers):
            return
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(build_log_format())
        self._logger.setLevel(get_log_level())
        self._logger.addHandler(consoleHandler)
        self._logger.propagate = False

    def info(self, message):
        self._logger.info(message)

    def error(self, message):
        self._logger.error(message)

import os
import logzero
import logging
from gunicorn.glogging import Logger

_log_level = os.environ.get("LOG_LEVEL", "info").upper()
log_level = getattr(logging, _log_level)
log_format = "%(color)s[%(levelname)1.1s %(asctime)s %(name)s]%(end_color)s %(message)s"

formatter = logzero.LogFormatter(fmt=log_format)
logger_args = dict(level=log_level, formatter=formatter)

logzero.__name__ = ""
logzero.setup_logger(**logger_args)
logzero.setup_default_logger(**logger_args)
logger = logzero.setup_logger("alertmanager_telegram", **logger_args)


class GunicornLogger(Logger):
    def __init__(self, cfg):
        super().__init__(cfg)

        self.error_log = logzero.setup_logger("gunicorn", **logger_args)

import logging

logger = logging.getLogger(__name__)


class AppLog:
    @classmethod
    def log_warning(cls):
        logger.warning("has has has")

    @classmethod
    def log_err(cls, msg):
        logger.debug(msg)

import datetime
import logging

logger = logging.getLogger(__name__)


class AppLog:
    @classmethod
    def log_warning(cls):
        logger.warning("This is log")

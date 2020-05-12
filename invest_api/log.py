import logging.config

from invest_api import settings
from invest_api.app import context

__all__ = (
    "app_logger",
    "access_logger",
    "setup_logging",
)

LEVEL = settings.LEVEL
DATETIME_FORMAT = settings.DATETIME_FORMAT

ACCESS_LOG_FORMAT = (
    'request_id="%{X-Request-Id}i" '
    'remote_addr="%a" '
    'referer="%{Referer}i" '
    'user_agent="%{User-Agent}i" '
    'protocol="%r" '
    'response_code="%s" '
    'request_time="%Tf" '
)

app_logger = logging.getLogger("app")
access_logger = logging.getLogger("access")
db_logger = logging.getLogger("db")


CONFIG = {
    "version": 1,
    'disable_existing_loggers': True,
    "loggers": {
        "root": {
            "level": LEVEL,
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        app_logger.name: {
            "level": LEVEL,
            "handlers": [
                "default",
            ],
            "propagate": False,
        },
        access_logger.name: {
            "level": LEVEL,
            "handlers": [
                "access",
            ],
            "propagate": False,
        },
        db_logger.name: {
            "level": LEVEL,
            "handlers": [
                "default",
            ],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": LEVEL,
            "handlers": [
                "default",
            ],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": LEVEL,
            "handlers": [
                "access",
            ],
            "propagate": False,
        },
    },
    "handlers": {
        "default": {
            "level": LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
                "request_id",
            ],
        },
        "console": {
            "level": LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
                "request_id",
            ],
        },
        "access": {
            "level": LEVEL,
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "filters": [
                "service_name",
            ],
        },
    },
    "formatters": {
        "default": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                'request_id="%(request_id)s" '
                'message="%(message)s" '
            ),
            "datefmt": DATETIME_FORMAT,
        },
        "access": {
            "format": (
                'time="%(asctime)s" '
                'level="%(levelname)s" '
                'logger="%(name)s" '
                'service_name="%(service_name)s" '
                'pid="%(process)d" '
                "%(message)s "
            ),
            "datefmt": DATETIME_FORMAT,
        },
    },
    "filters": {
        "service_name": {
            "()": "invest_api.log.ServiceNameFilter",
        },
        "request_id": {
            "()": "invest_api.log.RequestIDFilter",
        },
    },
}


class ServiceNameFilter(logging.Filter):

    def __init__(self, name: str = ""):
        self.service_name = settings.SERVICE_NAME

        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> int:
        setattr(record, "service_name", self.service_name)

        return super().filter(record)


class RequestIDFilter(logging.Filter):

    def __init__(self, name: str = ""):
        self.context_var = context.REQUEST_ID

        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> int:
        request_id = self.context_var.get("-")
        setattr(record, "request_id", request_id)

        return super().filter(record)


def setup_logging() -> None:
    logging.config.dictConfig(CONFIG)

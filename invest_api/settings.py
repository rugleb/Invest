from typing import Dict

from environs import Env

__all__ = ("env", "get_config")

env: Env = Env()

HOST = env.str("HOST", "127.0.0.1")
PORT = env.int("PORT", 8080)

SERVICE_NAME = env.str("SERVICE_NAME", "invest_api")

LEVEL = env.str("LOG_LEVEL", "INFO").upper()
DATETIME_FORMAT = env.str("LOG_DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")


def get_config() -> Dict:
    return {
        "db": {
            "pool": {
                "dsn": env.str("DB_URL", None),
                "min_size": env.int("DB_POOL_MIN_SIZE", 0),
                "max_size": env.int("DB_POOL_MAX_SIZE", 5),
                "max_queries": env.int("DB_POOL_MAX_QUERIES", 128),
                "timeout": env.float("DB_POOL_TIMEOUT", 5),
                "command_timeout": env.float("DB_POOL_COMMAND_TIMEOUT", 10),
            },
            "logger": {
                "name": "db",
            },
        },
    }

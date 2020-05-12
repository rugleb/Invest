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
    }

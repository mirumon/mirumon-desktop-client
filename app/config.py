import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings

from app.logging import InterceptHandler, format_record

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.joinpath(".env")
load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    server_websocket_url: str
    reconnect_delay: int
    debug: bool = False

    class Config:  # noqa: WPS431
        case_sensitive = True


settings = Settings()

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO

logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(
    handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL, "format": format_record}]
)
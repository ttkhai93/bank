import logging

from src.settings import app_settings
from src.app import create_app


logging.basicConfig(level=app_settings.LOG_LEVEL)
logging.getLogger("sqlalchemy.engine").setLevel(app_settings.LOG_LEVEL)

app = create_app()

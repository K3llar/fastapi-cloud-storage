from logging import config as logging_config

from pydantic import BaseSettings, EmailStr

from src.core.logger import LOGGING


class Settings(BaseSettings):
    app_title: str = 'Сервис для создания коротких ссылок'
    description: str = 'Сделай ссылку которой легко поделиться с друзьями!'
    secret: str
    database_url: str
    project_host: str
    project_port: str
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    class Config:
        env_file = '.env'


settings = Settings()

logging_config.dictConfig(LOGGING)

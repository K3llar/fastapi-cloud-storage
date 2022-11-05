from logging import config as logging_config

from pydantic import BaseSettings, EmailStr

from core.logger import LOGGING


class Settings(BaseSettings):
    app_title: str = 'Сервис для хранения личных файлов'
    description: str = 'Сохрани все что нужно'
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

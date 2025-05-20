import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    HLS_HOST_URL: str = os.getenv('HLS_HOST_URL')

    DB_HOST: str = os.getenv('POSTGRES_HOST')
    DB_PORT: int = os.getenv('POSTGRES_PORT')
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DB_DRIVER: str = os.getenv('POSTGRES_DRIVER')
    DB_NAME: str = os.getenv('POSTGRES_DB')

    CACHE_HOST: str = os.getenv('CACHE_HOST')
    CACHE_PORT: int = os.getenv('CACHE_PORT')
    CACHE_DB: int = os.getenv('CACHE_DB')
    CACHE_TTL_SECONDS: int = os.getenv('CACHE_TTL_SECONDS')

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

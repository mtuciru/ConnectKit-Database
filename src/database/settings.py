import enum
from typing import Optional

from pydantic_settings import BaseSettings


class Adapter(enum.Enum):
    postgresql = 'postgresql'
    mysql = 'mysql'
    sqlite = 'sqlite'


class Settings(BaseSettings):
    DB_ADDR: Optional[str] = None
    DB_PORT: int = 5432
    DB_ADAPTER: Adapter = Adapter.postgresql
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: Optional[str] = None
    DB_NAME: str = "postgres"
    DB_POOL_TIMEOUT: Optional[int] = 1
    DB_ECHO: bool = False


settings = Settings()

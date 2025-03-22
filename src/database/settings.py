import enum
from typing import Optional

from pydantic_settings import BaseSettings
from database.capability_check import (HAS_POSTGRESQL, HAS_ASYNC_POSTGRESQL,
                                       HAS_MARIADB, HAS_ASYNC_MARIADB)


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

if settings.DB_ADAPTER == Adapter.postgresql:
    if not (HAS_POSTGRESQL or HAS_ASYNC_POSTGRESQL):
        raise ImportError("psycopg adapter is not installed, but required. (DB_ADAPTER == postgresql)")
if settings.DB_ADAPTER == Adapter.mysql:
    if not (HAS_MARIADB or HAS_ASYNC_MARIADB):
        raise ImportError("mysqlclient or aiomysql adapters are not installed, but required. (DB_ADAPTER == mysql)")

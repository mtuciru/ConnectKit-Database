import enum
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from database.capability_check import (HAS_POSTGRESQL, HAS_ASYNC_POSTGRESQL,
                                       HAS_MARIADB, HAS_ASYNC_MARIADB)


class Adapter(enum.Enum):
    postgresql = 'postgresql'
    """
    PostgreSQL connection driver psycopg (sync and async)
    """
    mysql = 'mysql'
    """
    MySQL or MariaDB connection driver mysqlclient (sync) or aiomysql (async)
    """
    sqlite = 'sqlite'
    """
    SQLite connection driver sqlite3 (built-in, sync) or aiosqlite (async)
    """


class Settings(BaseSettings):
    """
    Database module configuration.

    Loaded from environ (priority) and .env top-level file.
    Configuration of module depends on these settings.
    Frozen when module is loaded.
    """
    model_config = SettingsConfigDict(env_prefix="db_",
                                      env_file='.env',
                                      env_file_encoding="utf-8",
                                      env_parse_none_str="",
                                      env_parse_enums=True,
                                      env_ignore_empty=False,
                                      extra="ignore",
                                      frozen=True,
                                      case_sensitive=False)
    addr: Optional[str] = None
    """
    Address for default db connection
    
    Address (ip or hostname) of default db connection.
    Ignored for sqlite driver.
    
    Default: None
    """
    port: int = 5432
    """
    Port for default db connection

    Port of default db connection.
    Ignored for sqlite driver.

    Default: 5432 (default postgresql port)
    """
    adapter: Adapter = Adapter.postgresql
    """
    Default db connection adapter library

    Select driver library for default db connection.

    Default: Adapter.postgresql
    """
    username: str = "postgres"
    """
    Username for default db connection

    User name to access db for default db connection.
    Ignored for sqlite driver.

    Default: "postgres"
    """
    password: Optional[str] = None
    """
    Password for default db connection

    User password to access db for default db connection.
    Ignored for sqlite driver.

    Default: None
    """
    name: str = "postgres"
    """
    Name of database
    
    Name of database for default db connection if database support this.
    For sqlite contains path to db file or :memory: (in memory database)
    
    Default: "postgres"
    """
    pool_recycle: Optional[int] = 3600
    """
    Pool recycle period for db driver sessions

    Set time in seconds after which the driver session will close.
    Ignored for sqlite driver.

    Default: 3600
    """
    echo: bool = False
    """
    Database echo mode.

    For debug purposes only. Print to log all sql statements.

    Default: False
    """


settings = Settings()

if settings.adapter == Adapter.postgresql:
    if not (HAS_POSTGRESQL or HAS_ASYNC_POSTGRESQL):
        raise ImportError("psycopg adapter is not installed, but required. (DB_ADAPTER == postgresql)")
if settings.adapter == Adapter.mysql:
    if not (HAS_MARIADB or HAS_ASYNC_MARIADB):
        raise ImportError("mysqlclient or aiomysql adapters are not installed, but required. (DB_ADAPTER == mysql)")

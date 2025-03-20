import enum
import json
from datetime import datetime
from functools import lru_cache
from typing import Any, Union

from pydantic import BaseModel
from sqlalchemy import URL

from database import errors
from database.capability_check import (HAS_ASYNC_SQLITE,
                                       HAS_POSTGRESQL, HAS_ASYNC_POSTGRESQL,
                                       HAS_MARIADB, HAS_ASYNC_MARIADB)
from database.settings import settings, Adapter


def get_default_url(asyncio=False):
    if settings.DB_ADAPTER != Adapter.sqlite:
        if settings.DB_ADDR is None or settings.DB_PORT is None:
            raise errors.DatabaseSettingsRequired(f"Specify default database environment agrs")
    else:
        if settings.DB_NAME is None:
            raise errors.DatabaseSettingsRequired(f"Specify default database environment agrs")
    return compile_url(settings.DB_ADAPTER, settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_ADDR,
                       settings.DB_PORT, settings.DB_NAME, asyncio)


@lru_cache()
def compile_url(adapter: Adapter, username: str, password: str, host: str, port: int, database: str, asyncio=False):
    if adapter == Adapter.postgresql:
        if not (HAS_POSTGRESQL or HAS_ASYNC_POSTGRESQL):
            raise ImportError("psycopg adapter is not installed, but required. (adapter == postgresql)")
        driver_name = "postgresql+psycopg"
    elif adapter == Adapter.mysql:
        if asyncio:
            if not HAS_ASYNC_MARIADB:
                raise ImportError(
                    "aiomysql adapter is not installed, but required. (adapter == mysql)")
        else:
            if not HAS_MARIADB:
                raise ImportError(
                    "mysqlclient adapter is not installed, but required. (adapter == mysql)")
        driver_name = f"mysql+{'aiomysql' if asyncio else 'mysqldb'}"
    elif adapter == Adapter.sqlite:
        if asyncio:
            if not HAS_ASYNC_SQLITE:
                raise ImportError("aiosqlite adapter is not installed, but required. (adapter == sqlite)")
        driver_name = f"sqlite+{'aiosqlite' if asyncio else 'pysqlite'}"
        username = None
        password = None
        host = None
        port = None
    else:
        raise errors.DatabaseWrongAdapterError(f'Adapter "{str(adapter)}" not exists.')
    return URL.create(
        driver_name,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def _json_default(obj: Any) -> Union[str, dict]:
    if isinstance(obj, enum.Enum):
        return str(obj.value)
    if isinstance(obj, datetime):
        if obj.tzinfo is None:
            obj = obj.astimezone()
        return obj.isoformat()
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    raise errors.DatabaseSerializationError(f"Can't serialize {type(obj)}")


def _custom_json_dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs, ensure_ascii=False, allow_nan=False, indent=None, separators=(',', ':'),
                      default=_json_default)

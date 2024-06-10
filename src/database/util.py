import enum
import json
from datetime import datetime
from functools import lru_cache
from typing import Any, Union

from pydantic import BaseModel
from sqlalchemy import URL

from database import errors
from database.settings import settings, Adapter


def get_default_url(asyncio=False):
    if settings.DB_ADDR is None or settings.DB_PORT is None:
        raise errors.DatabaseSettingsRequired(f"Specify default database environment agrs")
    return compile_url(settings.DB_ADAPTER, settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_ADDR,
                       settings.DB_PORT, settings.DB_NAME, asyncio)


@lru_cache()
def compile_url(adapter: Adapter, username: str, password: str, host: str, port: int, database: str, asyncio=False):
    if adapter == Adapter.postgresql:
        driver_name = f"postgresql+{'asyncpg' if asyncio else 'psycopg2'}"
    elif adapter == Adapter.mysql:
        driver_name = f"mysql+{'aiomysql' if asyncio else 'mysqldb'}"
    elif adapter == Adapter.sqlite:
        driver_name = f"sqlite+{'aiosqlite' if asyncio else 'pysqlite'}"
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

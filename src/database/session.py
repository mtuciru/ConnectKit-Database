import logging
from functools import lru_cache
from typing import Optional

import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine

import database.errors as errors
from database.util import compile_url, get_default_url, _custom_json_dumps, _custom_json_loads
from database.settings import settings, Adapter

logger = logging.getLogger("Database")


@lru_cache(maxsize=10)
def _create_engin(url: str):
    if str(url).startswith("sqlite"):
        return create_engine(url, json_serializer=_custom_json_dumps, json_deserializer=_custom_json_loads,
                             echo=settings.DB_ECHO)
    return create_engine(url, json_serializer=_custom_json_dumps, json_deserializer=_custom_json_loads,
                         pool_size=3, max_overflow=22, pool_timeout=settings.DB_POOL_RECYCLE,
                         pool_pre_ping=True, pool_use_lifo=True, echo=settings.DB_ECHO)


@lru_cache(maxsize=10)
def _get_sessionmaker(engine: Engine):
    return sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


@lru_cache(maxsize=1)
def get_default_engine() -> Engine:
    return _create_engin(get_default_url())


class Database:

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None,
                 host: Optional[str] = None, port: Optional[int] = None, database: Optional[str] = None,
                 adapter: Optional[Adapter] = None):
        if adapter is None:
            self._maker = _get_sessionmaker(get_default_engine())
        else:
            self._maker = _get_sessionmaker(
                _create_engin(compile_url(adapter, username, password, host, port, database, False)))

    def __enter__(self) -> Session:
        try:
            logger.info("Connecting to database...")
            self._session = self._maker()
            return self._session
        except sqlalchemy.exc.TimeoutError:
            logger.error("Connections pool is exhausted")
            raise errors.DatabaseOverloadError("Connections pool is exhausted")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning("Database rollback")
            self._session.rollback()
        else:
            logger.info("Database commit")
            self._session.commit()
        self._session.close()
        self._session = None
        logger.info("Database session closed")
        return False

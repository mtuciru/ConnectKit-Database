import logging
from functools import lru_cache
from typing import Optional

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

import database.errors as errors
from database.util import compile_url, get_default_url, _custom_json_dumps
from database.settings import settings, Adapter

logger = logging.getLogger("AsyncDatabase")


@lru_cache(maxsize=10)
def _create_async_engin(url: str):
    return create_async_engine(url, json_serializer=_custom_json_dumps,
                               pool_size=3, max_overflow=22, pool_timeout=settings.DB_POOL_TIMEOUT,
                               pool_pre_ping=True, pool_use_lifo=True, echo=settings.DB_ECHO)


@lru_cache(maxsize=10)
def _get_async_sessionmaker(engine: AsyncEngine):
    return async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


@lru_cache(maxsize=1)
def get_default_async_engine() -> AsyncEngine:
    return _create_async_engin(get_default_url(asyncio=True))


class AsyncDatabase:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None,
                 host: Optional[str] = None, port: Optional[int] = None, database: Optional[str] = None,
                 adapter: Optional[Adapter] = None):
        if adapter is None:
            self._maker = _get_async_sessionmaker(get_default_async_engine())
        else:
            self._maker = _get_async_sessionmaker(
                _create_async_engin(compile_url(adapter, username, password, host, port, database, True)))

    async def __aenter__(self) -> AsyncSession:
        try:
            logger.info("Connecting to database...")
            self._session = self._maker()
            return self._session
        except sqlalchemy.exc.TimeoutError:
            logger.error("Connections pool is exhausted")
            raise errors.DatabaseOverloadError("Connections pool is exhausted")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning("Database rollback")
            await self._session.rollback()
        else:
            logger.info("Database commit")
            await self._session.commit()
        await self._session.close()
        self._session = None
        logger.info("Database session closed")
        return False

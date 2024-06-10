from sqlalchemy import MetaData

from database.asyncio import get_default_async_engine


async def async_init_default_base(metadata: MetaData):
    async with get_default_async_engine().begin() as conn:
        await conn.run_sync(metadata.create_all)

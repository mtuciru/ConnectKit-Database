# ConnectKit Database [*en*|[ru](./README_RU.md)]

___

ConnectKit Database is a wrapper under SQLAlchemy with some utils.

Include pydantic settings, custom json serializer, template code.

## Installation

___

Three types of connectors are supported:

-[x] PostgreSQL (sync/async)
-[x] MySQL (MariaDB) (sync/async)
-[x] Sqlite3 (sync/async)

By default, the DB connector package is not installed (exclude default sqlite), extensions are specified for installation.

To install sync versions:

```shell
pip install ConnectKit-Database[postgresql]  # Установка коннектора PostgreSQL
pip install ConnectKit-Database[mysql]       # Установка коннектора MySQL/MariaDB
pip install ConnectKit-Database[all]         # Установка всех sync коннекторов
```

To install async versions:

```shell
pip install ConnectKit-Database[asyncpg]        # Установка коннектора PostgreSQL
pip install ConnectKit-Database[aiomysql]       # Установка коннектора MySQL/MariaDB
pip install ConnectKit-Database[aiosqlite]      # Установка коннектора Sqlite3
pip install ConnectKit-Database[asyncall]       # Установка всех async коннекторов
```

## Usage

___

Environment variables are used for connection by default.
Variables are extracted from the environment:

    DB_ADDR=  # Address for default connection to postgres or mysql(mariadb) (default: None)
    DB_PORT=5432  # Port for default connection to postgres or mysql(mariadb)
    DB_ADAPTER=postgresql  # Select default connection dialect (from postgresql, mysql and sqlite)
    DB_USERNAME=postgres  # Username for default connection postgres or mysql(mariadb)
    DB_PASSWORD=  # Username for default connection postgres or mysql(mariadb) (default: None)
    DB_NAME=postgres  # Database for postgres or mysql(mariadb), filepath for sqlite
    DB_POOL_TIMEOUT=1  # Global pool timeout for creating new session to DB
    DB_ECHO: bool = False  # Log all sql statements (for debug purposes)

These variables can be overridden:

```python
from database.settings import settings

settings.DB_ECHO = False
```

> **!! Attention !!**
After creating a default connection, changing the settings variables for it is ignored.

To open a connection, the `Database` and `AsyncDatabase` context managers are used:

```python
from database import Database, AsyncDatabase, AsyncSession

with Database() as db:
    db.execute(...)

async with AsyncDatabase() as db:
    await db.execute(...)


# For FastAPI:

async def db_dependency() -> AsyncSession:
    async with AsyncDatabase() as db:
        yield await db.execute(...)
```

The default Base can be used to create models:

```python
from database import Base
from sqlalchemy.orm import Mapped


class Model(Base):
    id: Mapped[int]
```

To initialize ORM models via Base for default connection:

```python
from database import init_default_base, async_init_default_base
from database import Base

init_default_base(Base.metadata)

await async_init_default_base(Base.metadata)
```

## License

___

ConnectKit Database is [MIT License](./LICENSE).
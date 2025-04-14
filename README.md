# ConnectKit Database [*en*|[ru](https://github.com/mtuciru/ConnectKit-Database/blob/2.2.1/README_RU.md)]

___

ConnectKit Database is a wrapper under SQLAlchemy with some utils.

Include pydantic settings, custom json serializer, template code.

## Installation

___

Three types of connectors are supported:

-[x] PostgreSQL (sync/async)
-[x] MySQL (MariaDB) (sync/async)
-[x] Sqlite3 (sync/async)

By default, the DB connector package is not installed (exclude built-in sqlite3), extras are specified for installation.

To install sync versions:

```shell
pip install ConnectKit-Database[postgresql]  # Install driver for PostgreSQL
```
```shell
pip install ConnectKit-Database[mysql]       # Install driver for MySQL/MariaDB
```
```shell
pip install ConnectKit-Database[all]         # Install all sync drivers
```

To install async versions:

```shell
pip install ConnectKit-Database[asyncpg]        # Install driver for PostgreSQL
```
```shell
pip install ConnectKit-Database[aiomysql]       # Install driver for MySQL/MariaDB
```
```shell
pip install ConnectKit-Database[aiosqlite]      # Install driver for Sqlite3
```
```shell
pip install ConnectKit-Database[asyncall]       # Install all async drivers
```

## Usage

___

Environment variables are used for connection by default.
Variables are extracted from the environment or `.env` file:

    DB_ADDR=               # Address for default connection to postgres or mysql(mariadb)
    DB_PORT=5432           # Port for default connection to postgres or mysql(mariadb)
    DB_ADAPTER=postgresql  # Select default connection dialect (from postgresql, mysql and sqlite)
    DB_USERNAME=postgres   # Username for default connection postgres or mysql(mariadb)
    DB_PASSWORD=           # Password for default connection postgres or mysql(mariadb)
    DB_NAME=postgres       # Database for postgres or mysql(mariadb), filepath for sqlite
    DB_POOL_RECYCLE=3600   # Global pool recycle timeout for driver session
    DB_ECHO: bool = False  # Global log all sql statements (for debug purposes)

These variables are frozen.

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

or via context managers:

```python
from database import Database, AsyncDatabase
from database import Base

Database().init_base(Base.metadata)

await (AsyncDatabase().init_base(Base.metadata))
```

## License

___

ConnectKit Database is [MIT License](https://github.com/mtuciru/ConnectKit-Database/blob/2.2.1/LICENSE).
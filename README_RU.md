# ConnectKit Database [[en](./README.md)|*ru*]

___

Connect Kit Database - это оболочка для SQLAlchemy с некоторыми функциями.

Включает в себя pydantic settings, пользовательский json-сериализатор, шаблонный код.

## Установка

___

Поддерживается три типа коннекторов:

-[x] PostgreSQL (sync/async)
-[x] MySQL (MariaDB) (sync/async)
-[x] Sqlite3 (sync/async)

По умолчанию, пакет коннектора к БД не устанавливаются, для установки указываются расширения.

Для установки sync версий:

```shell
pip install ConnectKit-Database[postgresql]  # Установка коннектора PostgreSQL
pip install ConnectKit-Database[mysql]       # Установка коннектора MySQL/MariaDB
pip install ConnectKit-Database[all]         # Установка всех sync коннекторов
```

Для установки async версий:

```shell
pip install ConnectKit-Database[asyncpg]     # Установка коннектора PostgreSQL
pip install ConnectKit-Database[aiomysql]    # Установка коннектора MySQL/MariaDB
pip install ConnectKit-Database[aiosqlite]   # Установка коннектора Sqlite3
pip install ConnectKit-Database[asyncall]    # Установка всех async коннекторов
```

## Использование

___

Для подключения по умолчанию используются переменные окружения.
Переменные извлекаются из environment:

    DB_ADDR=  # Address for default connection to postgres or mysql(mariadb) (default: None)
    DB_PORT=5432  # Port for default connection to postgres or mysql(mariadb)
    DB_ADAPTER=postgresql  # Select default connection dialect (from postgresql, mysql and sqlite)
    DB_USERNAME=postgres  # Username for default connection postgres or mysql(mariadb)
    DB_PASSWORD=  # Username for default connection postgres or mysql(mariadb) (default: None)
    DB_NAME=postgres  # Database for postgres or mysql(mariadb), filepath for sqlite
    DB_POOL_TIMEOUT=1  # Global pool timeout for creating new session to DB
    DB_ECHO: bool = False  # Log all sql statements (for debug purposes)

Данные переменные можно переопределить:

```python
from database.settings import settings

settings.DB_ECHO = False
```

**!! ВНИМАНИЕ !!**
После создания подключения по умолчанию, изменение параметров settings для него игнорируется.

Для открытия соединения используются `Database` и `AsyncDatabase` контекстные менеджеры:

```python
from database import Database, AsyncDatabase, AsyncSession

with Database() as db:
    db.execute(...)

async with AsyncDatabase() as db:
    await db.execute(...)


# Для FastAPI:

async def db_dependency() -> AsyncSession:
    async with AsyncDatabase() as db:
        yield await db.execute(...)
```

Для создания моделей может использоваться Base по умолчанию:

```python
from database import Base
from sqlalchemy.orm import Mapped


class Model(Base):
    id: Mapped[int]
```

Для инициализации моделей ORM через Base для подключения по умолчанию:

```python
from database import init_default_base, async_init_default_base
from database import Base

init_default_base(Base.metadata)

await async_init_default_base(Base.metadata)
```

## Лицензия

___

ConnectKit Database распространяется под [лицензией MIT](./LICENSE).
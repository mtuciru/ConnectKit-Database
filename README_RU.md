# ConnectKit Database [[en](https://github.com/mtuciru/ConnectKit-Database/blob/2.2.1/README.md)|*ru*]

___

ConnectKit Database - это оболочка для SQLAlchemy с некоторыми функциями.

Включает в себя pydantic settings, пользовательский json-сериализатор, шаблонный код.

## Установка

___

Поддерживается три типа коннекторов:

-[x] PostgreSQL (sync/async)
-[x] MySQL (MariaDB) (sync/async)
-[x] Sqlite3 (sync/async)

По умолчанию, пакет коннектора к БД не устанавливаются (за исключением стандартного sqlite3), для установки указываются
extra.

Для установки sync версий:

```shell
pip install ConnectKit-Database[postgresql]  # Установка коннектора PostgreSQL
```

```shell
pip install ConnectKit-Database[mysql]       # Установка коннектора MySQL/MariaDB
```

```shell
pip install ConnectKit-Database[all]         # Установка всех sync коннекторов
```

Для установки async версий:

```shell
pip install ConnectKit-Database[asyncpg]     # Установка коннектора PostgreSQL
```

```shell
pip install ConnectKit-Database[aiomysql]    # Установка коннектора MySQL/MariaDB
```

```shell
pip install ConnectKit-Database[aiosqlite]   # Установка коннектора Sqlite3
```

```shell
pip install ConnectKit-Database[asyncall]    # Установка всех async коннекторов
```

## Использование

___

Для подключения по умолчанию используются переменные окружения.
Переменные извлекаются из environment или файла `.env`:

    DB_ADDR=               # Адрес БД для postgres или mysql(mariadb)
    DB_PORT=5432           # Порт для БД postgres или mysql(mariadb) ()
    DB_ADAPTER=postgresql  # Выбор предустановленного диалекта БД (Из postgresql, mysql и sqlite)
    DB_USERNAME=postgres   # Имя пользователя для подключения к БД postgres или mysql(mariadb)
    DB_PASSWORD=           # Пароль пользователя для подключения к БД postgres или mysql(mariadb)
    DB_NAME=postgres       # Название базы данных postgres или mysql(mariadb), путь к БД для sqlite
    DB_POOL_RECYCLE=3600   # Глобальный таймаут для закрытия сессии БД.
    DB_ECHO: bool = False  # Логирование всех запросов sql (только для целей отладки)

Данные переменные заморожены:

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

или через контекстный менеджер:

```python
from database import Database, AsyncDatabase
from database import Base

Database().init_base(Base.metadata)

await (AsyncDatabase().init_base(Base.metadata))
```

## Лицензия

___

ConnectKit Database распространяется под [лицензией MIT](https://github.com/mtuciru/ConnectKit-Database/blob/2.2.1/LICENSE).
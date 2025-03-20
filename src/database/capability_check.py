# PostgreSQL adapter library
HAS_POSTGRESQL = False
HAS_ASYNC_POSTGRESQL = False
# MySQL (MariaDB) adapter library
HAS_MARIADB = False
HAS_ASYNC_MARIADB = False
# Sqlite adapter library
HAS_SQLITE = True
HAS_ASYNC_SQLITE = False

try:
    import psycopg

    HAS_POSTGRESQL = True
    HAS_ASYNC_POSTGRESQL = True
except ImportError:
    pass

try:
    import pymysql

    HAS_MARIADB = True
except ImportError:
    pass

try:
    import aiomysql

    HAS_ASYNC_MARIADB = True
except ImportError:
    pass

try:
    import aiosqlite

    HAS_ASYNC_SQLITE = True
except ImportError:
    pass

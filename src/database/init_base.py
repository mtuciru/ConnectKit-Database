from sqlalchemy import MetaData

from database.session import get_default_engine


def init_default_base(metadata: MetaData):
    metadata.create_all(get_default_engine())

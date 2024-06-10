class DatabaseError(Exception):
    pass


class DatabaseOverloadError(DatabaseError):
    pass


class DatabaseSerializationError(DatabaseError):
    pass


class DatabaseWrongAdapterError(DatabaseError):
    pass


class DatabaseSettingsRequired(DatabaseError):
    pass

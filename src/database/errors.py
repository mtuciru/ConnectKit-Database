class DatabaseError(Exception):
    pass


class DatabaseOverloadError(DatabaseError):
    pass


class DatabaseWrongAdapterError(DatabaseError):
    pass


class DatabaseSettingsRequired(DatabaseError):
    pass

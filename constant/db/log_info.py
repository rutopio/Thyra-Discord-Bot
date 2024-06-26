class DB_LOG_INFO():
    LOG_FOLDER_PATH = 'logs'
    LOG_FILE_FORMAT = 'json'

    TIME = 'time'

    STATUS = 'status'
    STATUS__EVENT = 'event'
    STATUS__GUILD_NAME = 'guild_name'
    STATUS__GUILD_ID = 'guild_id'

    USER = 'user'
    USER__NAME = 'user_name'
    USER__ID = 'user_id'
    USER__GUILD_NAME = 'guild_name'
    USER__GUILD_ID = 'guild_id'
    USER__KEY = 'key'

    ACTIVITY = 'activity'
    ACTIVITY__EVENT = 'event'
    ACTIVITY__DETAILS = 'details'
    ACTIVITY__GUILD_NAME = 'guild_name'
    ACTIVITY__GUILD_ID = 'guild_id'
    ACTIVITY__USER_NAME = 'user_name'
    ACTIVITY__USER_ID = 'user_id'

    ON_DASHBOARD_UPDATE_ERROR = 'on_dashboard_update_error'
    ON_READY = 'on_ready'
    ON_DISCONNECT = 'on_disconnect'
    ON_ERROR = 'on_error'
    ON_RESUMED = 'on_resumed'
    ON_GUILD_JOIN = 'on_guild_join'
    ON_GUILD_REMOVE = 'on_guild_remove'
    ON_INITIALIZED = 'on_initialized'

class DB_GUILD_INFO():
    ID = 'guild_id'
    NAME = 'guild_name'
    BOT_JOINED_AT = 'bot_joined_at'
    TIMEZONE = 'timezone'

    DASHBOARD_CH = 'dashboard_ch'
    DASHBOARD_CH__ID = 'channel_id'
    DASHBOARD_CH__ANNOUNCEMENT_ID = 'announcement_id'

    VERIFICATION_CH = 'verification_ch'
    VERIFICATION_CH__ID = DASHBOARD_CH__ID
    VERIFICATION_CH__ANNOUNCEMENT_ID = DASHBOARD_CH__ANNOUNCEMENT_ID

    KEYS_UID = 'uid'
    KEYS_INFO = 'keys'

    LOGS = 'logs'
    LOGS__USER_ID = 'user_id'
    LOGS__LOGGED_AT = 'logged_at'
    LOGS__EVENT = 'event'
    LOGS__DETAILS = 'details'

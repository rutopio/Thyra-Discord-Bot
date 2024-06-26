from enum import Enum


class CONTEXT_TYPE(str, Enum):
    EMBED_TITLE = 256
    EMBED_DESCRIPTION = 4096
    FIELD_NAME = 256
    FIELD_VALUE = 1024
    FOOTER = 2048
    AUTHOR_NAME = 256
    TOTAL = 6000
    FIXED = 200

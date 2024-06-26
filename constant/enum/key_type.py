from enum import Enum


class KEY_TYPE(str, Enum):
    ALL_KEYS = 'all'
    REGULAR_KEY = 'regular'
    LIMITED_KEY = 'limited'
    PROTECTED_KEY = 'protected'

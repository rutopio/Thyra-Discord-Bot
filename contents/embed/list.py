from constants.key_type_name import KEY_TYPE_NAME


class ListEmbedContent():
    regular_key_name = KEY_TYPE_NAME.REGULAR_KEYS_WITH_EMOJI
    regular_key_list_title = f'🪧 List of {KEY_TYPE_NAME.REGULAR_KEYS}'
    regular_key_list_description = f'Each {KEY_TYPE_NAME.REGULAR_KEY} can be used unlimited times.'

    limited_key_name = KEY_TYPE_NAME.LIMITED_KEYS_WITH_EMOJI
    limited_key_list_title = f'🪧 List of {KEY_TYPE_NAME.LIMITED_KEYS}'
    limited_key_list_description = f'Each {KEY_TYPE_NAME.LIMITED_KEY} can be used for fixed times.'

    protected_key_name = KEY_TYPE_NAME.PROTECTED_KEYS_WITH_EMOJI
    protected_key_list_title = f'🪧 List of {KEY_TYPE_NAME.PROTECTED_KEYS}'
    protected_key_list_description = 'User need to use both Key and PIN to access their roles.'

    all_keys_list_title = '🪧 List of Keys'
    all_keys_list_description = ''

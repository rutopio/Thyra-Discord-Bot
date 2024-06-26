from constants.key_type_name import KEY_TYPE_NAME


class ListCommandContent():
    # Commands Group
    list_commands_group_name = 'list'
    list_commands_group_description = 'Commands about listing Keys.'

    # List Regular Keys Command
    regular_key_command = 'regular-keys'
    regular_key_description = f'List {KEY_TYPE_NAME.REGULAR_KEYS}.'

    # List Limited Keys Command
    limited_key_command = 'limited-keys'
    limited_key_description = f'List {KEY_TYPE_NAME.LIMITED_KEYS}.'

    # List Protected Keys Command
    protected_key_command = 'protected-keys'
    protected_key_description = f'List {KEY_TYPE_NAME.PROTECTED_KEYS}.'

    # List All Keys Command
    all_key_command = 'all'
    all_key_description = 'List all Keys.'

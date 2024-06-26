from constants.key_type_name import KEY_TYPE_NAME


class CreateCommandContent():
    # Commands Group
    create_commands_group_name = 'create'
    create_commands_group_description = 'Commands about creating a new Key.'

    # Create a Regular Key Command
    regular_key_command = 'regular-key'
    regular_key_description = f'Create a {KEY_TYPE_NAME.REGULAR_KEY} that can be used an unlimited number of times.'
    regular_key_name_option = 'key_name'
    regular_key_name_option_description = 'Key Name. Users can use this Key to access their roles.'

    # Create a Limited Key Command
    limited_key_command = 'limited-key'
    limited_key_description = f'Create a {KEY_TYPE_NAME.LIMITED_KEY} that can be used for a limited number of times.'
    limited_key_name_option = 'key_name'
    limited_key_name_option_description = 'Key Name. Users can use this Key to access their roles.'
    limited_key_times_option = 'usage_limits'
    limited_key_times_option_description = 'How many times can the Key be used? Must be a positive number.'

    # Create a Protected Key Command
    protected_key_command = 'protected-key'
    protected_key_description = f'Create a {KEY_TYPE_NAME.PROTECTED_KEY} with One-Time PINs. User need to use both Key and PIN to access their roles.'
    protected_key_name_option = 'key_name'
    protected_key_name_option_description = 'Key Name. Users can use this Key to access their roles.'
    protected_key_number_option = 'num_otp'
    protected_key_number_option_description = 'How many One-Time PINs do you need? Must be a positive number.'

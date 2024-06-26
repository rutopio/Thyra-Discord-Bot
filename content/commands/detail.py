from constant.key_type_name import KEY_TYPE_NAME


class DetailCommandContent():
    # Commands Group
    detail_commands_group_name = 'detail'
    detail_commands_group_description = 'Commands about stats and details.'

    # Detail of Key Command
    detail_key_command = 'key'
    detail_key_description = f'Show the details of Key by name. Also show One-Time PINs for {KEY_TYPE_NAME.PROTECTED_KEY}.'
    detail_key_name_option = 'key_name'
    detail_key_name_option_description = 'Key name. Use /list command to find the Key.'

    # Detail of Member Command
    detail_member_command = 'member'
    detail_member_description = 'Show the details of Member by Id.'
    detail_member_name_option = 'member_id'
    detail_member_name_option_description = 'Member Id. Turn on Developer Mode then right-click on Member name and select Copy ID.'

    # Detail of PIN Command
    detail_pin_command = 'pin'
    detail_pin_description = f'Show the member details by PIN (for {KEY_TYPE_NAME.PROTECTED_KEY} only).'
    detail_pin_key_name_option = 'key_name'
    detail_pin_key_name_option_description = f'{KEY_TYPE_NAME.PROTECTED_KEY} Name.'
    detail_pin_name_option = 'pin'
    detail_pin_name_option_description = f'One-Time PIN associated with the {KEY_TYPE_NAME.PROTECTED_KEY}.'

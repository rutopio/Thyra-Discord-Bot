from utils import general


class KeyUtilsContent():
    separator = ', '
    none_mark = '-'
    inf_mark = '∞'

    active_string = 'Activate'
    inactive_string = 'Inactivate'

    active_emoji = ':arrow_forward:'
    inactive_emoji = ':pause_button:'

    left_member_string = '*Left Member*'

    def rename_log(old_name, new_name):
        return f'  - Rename from `{old_name}` to `{new_name}`\n'

    def UPDATE_STATUS_log(old_status, new_status):
        return f'  - Changed status from `{old_status}` to `{new_status}`\n'

    def adjust_times_log(old_val, new_val):
        return f'  - Changed usage limit from `{old_val}` to `{new_val}`\n'

    def gen_more_otps_log(number):
        return f'  - Generated new `{number}` {general.get_plural("PIN", number)} \n'

    def EDIT_ASSIGN_ROLES_roles_log(pre_roles_string, now_roles_string):
        return f'  - Edited Assign Roles from {pre_roles_string} to {now_roles_string}\n'

    def EDIT_REMOVE_ROLES_roles_log(pre_roles_string, now_roles_string):
        return f'  - Edited Remove Roles from {pre_roles_string} to {now_roles_string}\n'

    def omit_more(total_num, show_num):
        return f' (+{total_num-show_num} more)'

    def key_info_status(current_status):
        return f'- `[ Status ]` {current_status}\n'

    def key_info_type(key_type):
        return f'- `[   Type ]` {key_type}\n'

    def key_info_content(added_roles_content, remove_roles_content, member_counts):
        return f'- `[ Assign ]` {added_roles_content}\n- `[ Remove ]` {remove_roles_content}\n- `[   Used ]` {member_counts}'

    def key_info_creator(create_at_time, creator_mention):
        return f'\n- `[ Create ]` {create_at_time} by {creator_mention}'

    def used_key_order_protected(key_name, used_at, time_passed, used_order, max_count, used_pin):
        return f'```{key_name}```\n- `[ Used At  ]` {used_at} (+{time_passed})\n- `[ Used No. ]` {used_order} / {max_count}\n- `[ Used PIN ]` `{used_pin}`\n\n'

    def used_key_order(key_name, used_at, time_passed, max_count, used_order):
        return f'```{key_name}```\n- `[ Used At  ]` {used_at} (+{time_passed})\n- `[ Used No. ]` {used_order} / {max_count}\n\n'

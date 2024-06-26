from utils import general


class EditViewContent():
    keep_editing_button_id = '.edit_keep_editing_button'
    keep_editing_button_label = 'Keep Editing'
    keep_editing_button_emoji = '✍️'

    done_button_id = '.edit_done_button'
    done_button_label = 'Done'
    done_button_emoji = ''
    done_button_callback_content = 'Key edited successfully.'

    status_button_id = '.edit_activate_button'
    activate_button_label = 'Activate'
    activate_button_emoji = '▶️'
    inactivate_button_label = 'Inactivate'
    inactivate_button_emoji = '⏸'

    rename_key_button_id = '.edit_rename_key_button'
    rename_key_button_label = 'Rename Key'
    rename_key_button_emoji = '✏️'

    rename_key_modal_id = '.edit_rename_key_modal'
    rename_key_modal_title = 'Rename the Key'

    rename_key_modal_input_id = '.edit_rename_text_field'
    rename_key_modal_input_label = 'New Name'
    rename_key_modal_input_placeholder = ''

    adjust_usage_limit_button_id = '.edit_adjust_usage_limit_button'
    adjust_usage_limit_button_label = 'Adjust Usage Limit'
    adjust_usage_limit_button_emoji = '🔄'

    adjust_usage_limit_modal_id = '.edit_adjust_usage_limit_modal'
    adjust_usage_limit_modal_title = 'Adjust Usage Limit'

    adjust_usage_limit_modal_input_id = '.edit_new_usage_limit_input'
    adjust_usage_limit_modal_input_label = 'New Value'
    adjust_usage_limit_modal_input_placeholder = 'New value must be greater than current used times.'

    gen_more_otps_button_id = '.edit_more_pins_button'
    gen_more_otps_button_label = 'Gen More OTPs'
    gen_more_otps_button_emoji = '🆕'

    gen_more_otps_modal_id = '.edit_generate_more_pins_modal'
    gen_more_otps_modal_title = 'Generate More OTPs'

    gen_more_otps_modal_input_id = '.edit_generate_more_otp_input'
    gen_more_otps_modal_input_label = 'How many new OTPs do you need?'
    gen_more_otps_modal_input_placeholder = 'New PINs will be generated based on your input.'

    EDIT_ASSIGN_ROLES_role_button_id = '.EDIT_ASSIGN_ROLES_roles_button'
    EDIT_ASSIGN_ROLES_role_button_label = 'Edit Assign Roles'
    EDIT_ASSIGN_ROLES_role_button_emoji = '🌝'

    EDIT_REMOVE_ROLES_role_button_id = '.EDIT_REMOVE_ROLES_roles_button'
    EDIT_REMOVE_ROLES_role_button_label = 'Edit Remove Roles'
    EDIT_REMOVE_ROLES_role_button_emoji = '🌚'

    save_role_button_id = '.save_role_rules_button'
    save_role_button_id = '.save_role_rules_button'
    save_role_button_label = 'Save'
    save_role_button_emoji = '✅'

    def gen_more_otps_modal_attachment_name(key_name, total_value, current_value):
        return f'otp-({current_value + 1}-{total_value})-{key_name}'

    def gen_more_otps_callback_content(key_name, total_value, current_value, append_value):
        return f'New `{append_value}` One-Time {general.get_plural("PIN", append_value)} (`#{current_value+1}`~`#{total_value}`) for `{key_name}`:'

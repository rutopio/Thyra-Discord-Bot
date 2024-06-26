from constant.enum.context_type import CONTEXT_TYPE
from utils import general


class EditEmbedContent():
    none_string = '-'

    # Editing Embed - Main
    def editing_embed_title(key_name):
        content = f'✏️ Editing Key `{key_name}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def editing_embed_description(key_basic_info):
        return general.truncate_text(text=key_basic_info, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Editing Embed - Field 1
    def editing_embed_field_edited_history_name():
        content = 'Edited History (Latest 5 records)'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def editing_embed_field_edited_history_value(history_log):
        return general.truncate_text(text=history_log, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Renamed Embed - Main
    def renamed_embed_title(old_key_name):
        content = f'⬆️ Key `{old_key_name}` has been renamed'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def renamed_embed_description(new_key_name):
        content = f'- Please use new name `{new_key_name}` from now.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Adjusted Embed - Main
    def adjusted_embed_title(key_name):
        content = f'⬆️ Key `{key_name}` has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def adjusted_embed_description(old_times_value, new_times_value):
        content = f'- The usage limit has been updated from `{old_times_value}` to `{new_times_value}`.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Generate More Otp Embed - Main
    def generated_more_otp_embed_title(key_name):
        content = f'⬆️ Key `{key_name}` has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def generated_more_otp_embed_description(num_additional_pins):
        content = f'- Generate {num_additional_pins} new {general.get_plural("PIN", num_additional_pins)}.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Change Status Embed - Main
    active_string = 'Activated'

    inactive_string = 'Inactivated'

    def changed_status_embed_title(key_name, status_name):
        content = f'⬆️ Key `{key_name}` has been {status_name}'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def changed_status_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Updated Role Rules - Main
    def updated_role_rules_embed_title(key_name):
        content = f'⬆️ Key `{key_name}` has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def updated_role_rules_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Updated Role Rules - Field 1

    def updated_role_rules_embed_field_update_type_name():
        content = 'Updated Type'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def updated_role_rules_embed_field_update_type_value(updated_type):
        content = f'{updated_type.capitalize()} Roles'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Updated Role Rules - Field 2

    def updated_role_rules_embed_field_previous_roles_name():
        content = 'Previous Rules'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def updated_role_rules_embed_field_previous_roles_value(before_roles_mentions_content):
        return general.truncate_text(text=before_roles_mentions_content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Updated Role Rules - Field 3

    def updated_role_rules_embed_field_new_roles_name():
        content = 'New Rules'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def updated_role_rules_embed_field_new_roles_value(after_roles_mentions_content):
        return general.truncate_text(text=after_roles_mentions_content, content_type=CONTEXT_TYPE.FIELD_VALUE)

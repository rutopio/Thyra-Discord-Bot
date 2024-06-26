from constant.enum.context_type import CONTEXT_TYPE
from constant.key_type_name import KEY_TYPE_NAME
from utils import general


class RemoveEmbedContent():
    # Removing a Key Embed - Main
    def removing_key_embed_title(key_name):
        content = f'😥 Are you sure to remove Key `{key_name}`?'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def removing_key_embed_description(role_message):
        return general.truncate_text(text=role_message, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Removing a Key Embed - Field 1
    def removing_key_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def removing_key_embed_field_note_value():
        content = '1. This command is irreversible.\n2. After removing this Key, all logs and statistics related to it will be removed as well.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Removing a Key Embed - Field 2
    def removing_key_embed_field_about_otp_name():
        content = 'About OTPs'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def removing_key_embed_field_about_otp_value():
        content = f'- After removing this Key, if the same name {KEY_TYPE_NAME.PROTECTED_KEY} is re-created, the PINs will be regenerated.\n- All existing PINs will become invalid.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Removing All Check Embed - Main
    def removing_all_check_embed_title():
        content = '😥 Are you sure to remove ALL Keys?'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def removing_all_check_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def removing_all_check_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def removing_all_check_embed_field_note_value():
        content = '1. **This command is irreversible.**\n2. After removing the Key, all logs and statistics related to it will be removed as well.\n3. Even if the same name Key is re-created, One-Time PINs will be regenerated, all existing PINs will become invalid.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Removed a Key Embed - Main
    def removed_key_embed_title(key_name):
        content = f'🗑 Key `{key_name}` has been removed'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def removed_key_embed_description():
        content = '- This command is irreversible.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Removed All Embed - Main
    def removed_all_embed_title():
        content = '🗑 All Keys have been removed'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def removed_all_embed_description():
        content = '- This command is irreversible.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

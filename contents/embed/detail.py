from constants.enum.context_type import CONTEXT_TYPE

from contents.commands.list import ListCommandContent
from contents.commands.detail import DetailCommandContent
from utils import general


class DetailEmbedContent():
    # Key Details Embed - Main
    def key_details_embed_title(key_name):
        content = f'🪧 Detail of Key `{key_name}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def key_details_embed_description(key_basic_info):
        return general.truncate_text(text=key_basic_info, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Key Details Embed - Field 1

    def key_details_embed_field_edited_history_name():
        content = 'Edited History (Latest 5 records)'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def key_details_embed_field_edited_history_value(history_log):
        return general.truncate_text(text=history_log, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Invalid User Id Embed - Main
    def invalid_user_id_embed_title():
        content = '❌ Invalid member ID or user has left'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_user_id_embed_description(member_id):
        content = f'- Your input: `{member_id}`\n- The member ID is incorrect or invalid, the user account has been deleted, or the user is no longer in this server.\n- Make sure you have enabled *User Settings > Advanced > Developer Mode*, then right-click on the member name and select *Copy User ID*.\n- You can only search the details of members who are currently in this server.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Key Type Not Protected Embed - Main
    def key_type_not_protected_embed_title(key_name):
        content = f'❌ {key_name} is not Protected Key'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def key_type_not_protected_embed_description():
        content = f'Please use `/{ListCommandContent.list_commands_group_name} {ListCommandContent.protected_key_command}` to check the name of Key.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Pin Related Key Embed - Main
    def pin_related_key_embed_used_title(key_name, pin_code):
        content = f'👤 Member who used Key `{key_name}` with PIN `{pin_code}` '
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def pin_related_key_embed_unused_title(key_name, pin_code):
        content = f'❌ PIN `{pin_code}` for Key `{key_name}` has not been used yet'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def pin_related_key_embed_unused_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def pin_related_key_embed_invalid_title(key_name, pin_code):
        content = f'❌ PIN `{pin_code}` is invalid for Key `{key_name}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def pin_related_key_embed_invalid_description():
        content = f'- Please use `/{DetailCommandContent.detail_commands_group_name} {DetailCommandContent.detail_key_command} <key_name>` to find used and unused PINs.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # User Details Embed - Main
    def user_details_embed_title(username):
        content = f'🪧 Detail of Member `{username}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def user_details_embed_description(key_content):
        return general.truncate_text(text=key_content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # User Details Embed - Field 1
    def user_details_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def user_details_embed_field_note_value():
        content = '1. Only display existing Keys, including both activated and inactivated ones.\n2. The time in Key used time brackets indicates *how long after the user joined the server they used the Key*.\n3. The number in `[ Used No. ]` row represents *Users Used Order / Total Used / Usage limit*. '
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # User Details Embed - Field 2

    def user_details_embed_field_member_info_name():
        content = 'Member Info'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def user_details_embed_field_member_info_value(user_info_content):
        return general.truncate_text(text=user_info_content, content_type=CONTEXT_TYPE.FIELD_VALUE)

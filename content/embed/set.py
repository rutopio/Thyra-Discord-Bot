from constant.constants import CONSTANT
from constant.enum.context_type import CONTEXT_TYPE
from utils import general


class SetEmbedContent():
    # Welcome Embed After Verify - Main
    def welcome_embed_after_verify_title():
        content = '🎉 Your roles have been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def welcome_embed_after_verify_description(added_roles_mentions):
        content = f'- Your new roles: {", ".join(added_roles_mentions)}' if added_roles_mentions else ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Invalid Key Or Pin Embed - Main
    def invalid_key_or_pin_embed_title():
        content = '😥 Authentication failed'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_key_or_pin_embed_description(user):
        content = f'{user.mention}, please try again.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def invalid_key_or_pin_embed_field_reasons_name():
        content = 'Possible Reasons'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def invalid_key_or_pin_embed_field_reasons_value():
        content = '1. The Key or PIN you entered is incorrect.\n2. The Key does not need PIN. Just leave PIN field blank.\n3. The Key has already reached its usage limit or been used before.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Hi There Embed - Main
    def hi_there_embed_title():
        content = '👋 Hi, there!'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def hi_there_embed_description():
        content = '**Click the button below to access roles by your Key.**'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def hi_there_embed_footer():
        content = 'Powered by Thyra'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FOOTER)

    # Verification Channel Updated Embed - Main
    def verification_channel_updated_embed_title():
        content = '✅ Verification channel has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def verification_channel_updated_embed_description(channel_mention):
        content = f'The Verification Dialog has been set at {channel_mention} channel.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Dashboard Channel Updated Embed - Main
    def dashboard_channel_updated_embed_title():
        content = '✅ Dashboard channel has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def dashboard_channel_updated_embed_description(channel_mention):
        content = f'📍 From now, Thyra will use {channel_mention} channel as dashboard.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Dashboard Channel Setting Embed - Main
    def dashboard_channel_setting_embed_title():
        content = '⚙️ Select a channel for dashboard and logging'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def dashboard_channel_setting_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def dashboard_channel_setting_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def dashboard_channel_setting_embed_field_note_value():
        content = '1. Selector might not display all channels at once. Please type your channel name to search.\n2. One Dashboard Channel per server.\n3. We strongly recommend setting channel permissions to allow only administrators to view it.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Verification Channel Setting Embed - Main
    def verification_channel_setting_embed_title():
        content = '⚙️ Select a channel for verification dialog'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def verification_channel_setting_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def verification_channel_setting_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def verification_channel_setting_embed_field_note_value():
        content = '1. Selector might not display all channels at once. Please type your channel name to search.\n2. One Verification Dialog per server. Once you create a new one, the previous one will be deleted.\n3. You can place the Dialog in your Welcome Channel.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # User Used Key Before Embed - Main
    def user_used_key_before_embed_title():
        content = '🎓 You have already used this Key before'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def user_used_key_before_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Invalid Timezone Embed - Main
    def invalid_timezone_embed_title():
        content = '❌ Invalid value'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_timezone_embed_description(value):
        content = f'- Your input: `{value}`\n- The `timezone` format is incorrect.\n- The format should be `±[hh][mm]` (with symbol). For example, `-0800`, `+1200`, `+0530`.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Valid Timezone Embed - Main
    def valid_timezone_embed_title():
        content = '✅ Log time zone has been updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def valid_timezone_embed_description(timezone, localtime):
        content = f'- The display time zone has been set to `{timezone}`.\n- Your local time should be `{localtime.strftime(CONSTANT.DATE_FORMAT)}`.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

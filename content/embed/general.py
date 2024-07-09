from constant.enum.context_type import CONTEXT_TYPE
from constant.usage_limits import USAGE_LIMIT
from content.commands.edit import EditCommandContent
from content.commands.list import ListCommandContent
from utils import general


class GeneralEmbedContent():
    # Invalid Usage Limit Embed - Main
    def invalid_usage_limit_embed_title():
        content = '❌ Invalid value'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_usage_limit_embed_description():
        content = '- The number of Usage Limits must be a positive integer.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Invalid Otp Number Embed - Main
    def invalid_otp_number_embed_title():
        content = '❌ Invalid value'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_otp_number_embed_description(value):
        content = f'- Your input: `{value}`\n- The number of One-Time PINs must be a positive integer.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Invalid Value Embed - Main
    def invalid_value_embed_title():
        content = '❌ Invalid value'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def invalid_value_embed_description(value):
        content = f'- Your input: `{value}`\n- New value must be a positive integer.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # New Usage Limit Too Small Embed - Main
    def new_usage_limit_too_small_embed_title():
        content = '❌ Invalid value'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def new_usage_limit_too_small_embed_description(num_used_users, new_times_value):
        content = f'- Your input: `{new_times_value}`\n- New usage limits must not be less than current used times (`{num_used_users}`).'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Name Too Long Embed - Main
    def name_too_long_embed_title():
        content = '❌ Key name is too long'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def name_too_long_embed_description(key_name):
        content = f'- Your input: `{key_name}`\n- Length of Key name must be less than `{USAGE_LIMIT.MAX_LENGTH_OF_KEY_NAME()}` letters. Current length: `{len(key_name)}`.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Key Is Full Embed - Main
    def key_is_full_embed_title():
        content = '❌ Key quota exceeded'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def key_is_full_embed_description():
        content = f'- The number of Keys has reached the quota (up to `{USAGE_LIMIT.MAX_NUMBER_OF_KEY_PER_TYPE()}` Keys for each type).'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Usage Limit Too Many Embed - Main
    def usage_limit_too_many_embed_title():
        content = '❌ Usage limits exceeded'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def usage_limit_too_many_embed_description(number):
        content = f'- Your input: `{number}`\n- The usage limit for the Key can only be set up to `{USAGE_LIMIT.MAX_NUMBER_OF_KEY_USAGE_LIMIT()}` times.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # OTP Too Many Embed - Main
    def otp_too_many_embed_title():
        content = '❌ PIN quota exceeded'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def otp_too_many_embed_description(number):
        content = f'- Your input: `{number}`\n- A Key can only generate up to `{USAGE_LIMIT.MAX_NUMBER_OF_PINS()}` One-Time PINs.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Edited OTP Too Many Embed - Main
    def edited_otp_too_many_embed_title():
        content = '❌ PIN quota exceeded'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def edited_otp_too_many_embed_description(num_current_pins, num_additional_pins):
        content = f'- Your input: `{num_additional_pins}`\n- A Key can only generate up to `{USAGE_LIMIT.MAX_NUMBER_OF_PINS()}` One-Time PINs.\n- Currently the Key has `{num_current_pins}` {general.get_plural("OTP", num_current_pins)}. It can generate up to `{USAGE_LIMIT.MAX_NUMBER_OF_PINS()-num_current_pins}` more {general.get_plural("OTP", num_current_pins)}.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Key Not Found Embed
    def key_not_found_embed_title(key_name):
        content = f'❌ Key `{key_name}` does not exists'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def key_not_found_embed_description():
        content = f'- Please use `/{ListCommandContent.list_commands_group_name} {ListCommandContent.all_key_command}` to find the name of Key.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    # Same Key Name Exist Embed - Main
    def same_key_name_exist_embed_title(key_name):
        content = f'❌ Key `{key_name}` already exists'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def same_key_name_exist_embed_description():
        content = f'- Please use another name or rename the original one by `/{EditCommandContent.edit_commands_group_name} <key_name>` command.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def no_permission_response():
        return 'Sorry, you do not have permissions to access this command.'

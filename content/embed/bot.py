from constant.enum.context_type import CONTEXT_TYPE
from constant.key_type_name import KEY_TYPE_NAME
from content.commands.create import CreateCommandContent
from content.commands.edit import EditCommandContent
from content.commands.detail import DetailCommandContent
from content.commands.remove import RemoveCommandContent
from content.commands.list import ListCommandContent
from content.commands.set import SetCommandContent
from utils import general


class BotEmbedContent():
    active_emoji = ':arrow_forward:'
    inactive_emoji = ':pause_button:'

    def used_users_counter(used_num, max_num=None):
        if max_num:
            return f'{used_num} / {max_num}'
        else:
            return f'{used_num}'

    #  Bot Dashboard Embed - Main
    def bot_dashboard_embed_title():
        content = '🎛️ Thyra Bot Dashboard'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def bot_dashboard_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    #  Bot Dashboard Embed - Field 1 - Timezone
    def bot_dashboard_embed_field_timezone_name():
        content = 'Time Zone'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_timezone_value(timezone_offset):
        content = f'`UTC {timezone_offset[:3]}:{timezone_offset[3:]}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 2 - Verification Ch.
    def bot_dashboard_embed_field_verification_ch_name():
        content = 'Verification Ch.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_verification_ch_if_invalid():
        content = 'Not set yet, or has been deleted.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    def bot_dashboard_embed_field_verification_ch_value():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 3 - Number of Members
    def bot_dashboard_embed_field_num_member_name():
        content = '# Members'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_num_member_value(guild):
        content = f'`{len([m for m in guild.members if not m.bot])}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 4 - Number of Bots
    def bot_dashboard_embed_field_num_bot_name():
        content = '# Bots'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field__num_bot_value(guild):
        content = f'`{len([m for m in guild.members if m.bot])}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 5 - Number of Roles
    def bot_dashboard_embed_field_num_role_name():
        content = '# Roles'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_num_role_value(guild):
        content = f'`{len(guild.roles)}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 6 - Regular Keys
    def bot_dashboard_embed_field_regular_key_name(regular_key_names):
        content = f'{KEY_TYPE_NAME.REGULAR_KEYS_WITH_EMOJI} - {len(regular_key_names)}'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_regular_key_value(content):
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 7 - Limited Keys
    def bot_dashboard_embed_field_limited_key_name(limited_key_names):
        content = f'{KEY_TYPE_NAME.LIMITED_KEYS_WITH_EMOJI} - {len(limited_key_names)}'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_limited_key_value(content):
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Field 8 - Protected Keys
    def bot_dashboard_embed_field_protected_name(protected_key_names):
        content = f'{KEY_TYPE_NAME.PROTECTED_KEYS_WITH_EMOJI} - {len(protected_key_names)}'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_dashboard_embed_field_protected_value(content):
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    #  Bot Dashboard Embed - Footer
    def bot_dashboard_embed_footer():
        content = 'Latest Updated'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FOOTER)

    # Bot Log Embed - Main
    def bot_log_embed_title():
        content = '🪵 Server Logs (Auto Refresh)'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def bot_log_embed_description(content):
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def editor_mention_if_user_invalid():
        return '*Left Member*'

    def set_timezone_string(details):
        return f'⏳ Set Time Zone | `{details}`'

    def create_key_string(details):
        return f'➕ Create Key | `{details[0]}` [ {details[1].capitalize()} ]'

    def edit_status_string(details):
        new_status_content = 'Activate' if details[1] else 'Inactivate'
        return f'➕ Edit Key | `{details[0]}` [ {new_status_content} ]'

    def edit_name_string(details):
        return f'➕ Edit Key | `{details[0]}` [ Rename to `{details[1]}` ]'

    def EDIT_USAGE_COUNT_string(details):
        return f'➕ Edit Key | `{details[0]}` [ Adjust usage limit to `{details[1]}` ]'

    def edit_gen_otp_string(details):
        return f'➕ Edit Key | `{details[0]}` [ Gen `{details[1]}` new {general.get_plural("OTP", details[1])} ]'

    def EDIT_ASSIGN_ROLES_string(details):
        return f'➕ Edit Key | `{details}` [ Update Assign Role Rules ]'

    def EDIT_REMOVE_ROLES_string(details):
        return f'➕ Edit Key | `{details}` [ Update Remove Role Rules ]'

    def remove_all_string(details):
        return '🗑 Remove All Keys'

    def remove_key_string(details):
        return f'🗑 Remove Key | `{details}`'

    def set_dashboard_string(details):
        return f'🪧 Set Dashboard Ch.| {details}'

    def set_verification_string(details):
        return f'🪧 Set Verification Ch. | {details}'

    # Bot Tutorial Embed - Main
    def bot_tutorial_embed_title():
        content = '🤖 Thyra Bot Tutorial'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def bot_tutorial_embed_description():
        content = '''Thyra can assist your server in automatically assigning or removing roles to members based on unique Keys. 
You can restrict access to certain private channels and create a Key for specific roles within your server. Once members input the Key, they can access the roles and channels you've designated for them. 
'''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    def bot_tutorial_embed_url():
        return 'https://thyra.pages.dev'

    ## Bot Tutorial Embed - Field 1

    def bot_tutorial_embed_field_quick_start_name():
        content = 'Quick Start'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_tutorial_embed_field_quick_start_value():
        content = f'''
1. **Move Thyra's role higher than the other roles you want to set in the server Role list** (*Server Settings > Roles*).
2. Use `/{CreateCommandContent.create_commands_group_name} {CreateCommandContent.regular_key_command} <key_name>` to create a Regular Key.
3. Use `/{SetCommandContent.set_commands_group_name} {SetCommandContent.set_verification_command}` to set the verification channel, such as your Welcome Channel.
4. Share the Key with others. That's all!
'''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Bot Tutorial Embed - Field 2

    def bot_tutorial_embed_field_commands_name():
        content = 'Commands (Admin only, Ephemeral responses)'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def bot_tutorial_embed_field_commands_value():
        content = f'''
> Create a Key
- `/{CreateCommandContent.create_commands_group_name} {CreateCommandContent.regular_key_command} <key_name>`
- `/{CreateCommandContent.create_commands_group_name} {CreateCommandContent.limited_key_command} <key_name> <max_used>`
- `/{CreateCommandContent.create_commands_group_name} {CreateCommandContent.protected_key_command} <key_name> <num_otp>`

> Edit a Key (Rename, edit Role Rules, etc.)
- `/{EditCommandContent.edit_commands_group_name} <key_name>`

> Show Key details, One-Time PINs, and Member
- `/{DetailCommandContent.detail_commands_group_name} {DetailCommandContent.detail_key_command} <key_name>`: Also list the One-Time PINs for {KEY_TYPE_NAME.PROTECTED_KEY}.
- `/{DetailCommandContent.detail_commands_group_name} {DetailCommandContent.detail_member_command} <member_id>`: Only server member available.
- `/{DetailCommandContent.detail_commands_group_name} {DetailCommandContent.detail_pin_command} <key_name> <pin>`: Only {KEY_TYPE_NAME.PROTECTED_KEY} available.

>  Remove a Key
- `/{RemoveCommandContent.remove_commands_group_name} {RemoveCommandContent.remove_key_command} <key_name>`
- `/{RemoveCommandContent.remove_commands_group_name} {RemoveCommandContent.remove_all_command}`

> List Keys
- `/{ListCommandContent.list_commands_group_name} {ListCommandContent.list_commands_group_name}`
- `/{ListCommandContent.list_commands_group_name} {ListCommandContent.regular_key_command}`
- `/{ListCommandContent.list_commands_group_name} {ListCommandContent.limited_key_command}`
- `/{ListCommandContent.list_commands_group_name} {ListCommandContent.protected_key_command}`

> Set Channels and time zone
- `/{SetCommandContent.set_commands_group_name} {SetCommandContent.set_verification_command}`: {SetCommandContent.set_verification_description}
- `/{SetCommandContent.set_commands_group_name} {SetCommandContent.set_dashboard_command}`: {SetCommandContent.set_dashboard_description} By default, Thyra will use *this* channel.
- `/{SetCommandContent.set_commands_group_name} {SetCommandContent.set_timezone_command} <timezone>`: {SetCommandContent.set_timezone_description}
'''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    def dashboard_updated_embed_title():
        return '✅ Dashboard updated!'

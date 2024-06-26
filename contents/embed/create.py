from constants.enum.context_type import CONTEXT_TYPE
from contents.commands.edit import EditCommandContent
from utils import general


class CreateEmbedContent():
    # Creating Embed - Main
    def creating_embed_title(key_name):
        content = f'✏️ Creating Key: `{key_name}`'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def creating_embed_description():
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Creating Embed - Field 1
    def creating_embed_field_key_type_name():
        content = 'Key Type'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def creating_embed_field_key_type_value(type_description):
        return general.truncate_text(text=type_description, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Creating Embed - Field 2
    def creating_embed_field_note_name():
        content = 'Notes'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def creating_embed_field_note_value():
        content = f'1. Name and Role Rule can be edited later by using `/{EditCommandContent.edit_commands_group_name} <key_name>` command, but the Key Type cannot be changed.\n2. Selector might not display all Roles at once. Please type your Role names to search.\n3. Both fields are **optional** and can be left empty.\n4. Roles managed by integrations or bots can not be assigned to Members.'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    # Created Embed - Main
    def created_embed_title(key_name):
        content = f'🆕 Key `{key_name}` has been created'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_TITLE)

    def created_embed_description(key_name):
        content = ''
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.EMBED_DESCRIPTION)

    ## Created Embed - Field 1
    def created_embed_field_key_type_name():
        content = 'Key Type'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def created_embed_field_key_type_value(type_description):
        return general.truncate_text(text=type_description, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Created Embed - Field 2

    def created_embed_field_assign_roles_name():
        content = 'Roles to Assign'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def created_embed_field_assign_roles_value(added_roles_content):
        return general.truncate_text(text=added_roles_content, content_type=CONTEXT_TYPE.FIELD_VALUE)

    ## Created Embed - Field 3

    def created_embed_field_remove_roles_name():
        content = 'Roles to Remove'
        return general.truncate_text(text=content, content_type=CONTEXT_TYPE.FIELD_NAME)

    def created_embed_field_remove_roles_value(remove_roles_content):
        return general.truncate_text(text=remove_roles_content, content_type=CONTEXT_TYPE.FIELD_VALUE)

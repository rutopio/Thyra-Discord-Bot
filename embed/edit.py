import discord

from contents.embed.edit import EditEmbedContent

from constants.constants import CONSTANT
from constants.db.key_info import DB_KEY_INFO
from constants.edit_operation import EDIT_OPERATION
from utils.role import RoleUtils
from utils.key import KeyUtils


class EditEmbed():

    def get_editing_embed(ctx, key_info, show_history=True):
        key_name, key_basic_info, history_log = KeyUtils.get_key_info_content(ctx, key_info, show_history=True)
        this_embed = discord.Embed(
            title=EditEmbedContent.editing_embed_title(key_name=key_name),
            description=EditEmbedContent.editing_embed_description(key_basic_info=key_basic_info),
            color=CONSTANT.EMBED_COLOR,
        )
        if show_history and history_log:
            this_embed.add_field(
                name=EditEmbedContent.editing_embed_field_edited_history_name(),
                value=EditEmbedContent.editing_embed_field_edited_history_value(history_log=history_log),
                inline=False,
            )
        return this_embed

    def get_renamed_embed(old_key_name, new_key_name):
        return discord.Embed(
            title=EditEmbedContent.renamed_embed_title(old_key_name=old_key_name),
            description=EditEmbedContent.renamed_embed_description(new_key_name=new_key_name),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_adjusted_embed(key_info, old_times_value, new_times_value):
        key_name = key_info[DB_KEY_INFO.NAME]
        this_embed = discord.Embed(
            title=EditEmbedContent.adjusted_embed_title(key_name=key_name),
            description=EditEmbedContent.adjusted_embed_description(
                old_times_value=old_times_value,
                new_times_value=new_times_value,
            ),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_generated_more_otp_embed(key_info, num_additional_pins):
        key_name = key_info[DB_KEY_INFO.NAME]
        this_embed = discord.Embed(
            title=EditEmbedContent.generated_more_otp_embed_title(key_name=key_name),
            description=EditEmbedContent.generated_more_otp_embed_description(num_additional_pins=num_additional_pins),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_changed_status_embed(key_info, status_new):
        status_name = EditEmbedContent.active_string if status_new else EditEmbedContent.inactive_string
        key_name = key_info[DB_KEY_INFO.NAME]
        this_embed = discord.Embed(
            title=EditEmbedContent.changed_status_embed_title(key_name=key_name, status_name=status_name),
            description=EditEmbedContent.changed_status_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_updated_role_rules_embed(interaction, key_info, updated_roles, updated_type):
        key_name = key_info[DB_KEY_INFO.NAME]
        before_roles = key_info[
            DB_KEY_INFO.ASSIGN_ROLES] if updated_type == EDIT_OPERATION.UPDATE_ASSIGN_ROLES else key_info[
                DB_KEY_INFO.REMOVE_ROLES]
        before_roles_mentions = RoleUtils.get_roles_mention_list(interaction, before_roles)

        before_roles_mentions_content = '\n'.join(['- ' + item for item in before_roles_mentions
                                                   ]) if before_roles_mentions else EditEmbedContent.none_string

        after_roles_mentions = RoleUtils.get_roles_mention_list(interaction, updated_roles)
        after_roles_mentions_content = '\n'.join(['- ' + item for item in after_roles_mentions
                                                  ]) if after_roles_mentions else EditEmbedContent.none_string

        this_embed = discord.Embed(
            title=EditEmbedContent.updated_role_rules_embed_title(key_name=key_name),
            description=EditEmbedContent.updated_role_rules_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=EditEmbedContent.updated_role_rules_embed_field_update_type_name(),
            value=EditEmbedContent.updated_role_rules_embed_field_update_type_value(updated_type=updated_type),
            inline=False,
        )
        this_embed.add_field(
            name=EditEmbedContent.updated_role_rules_embed_field_previous_roles_name(),
            value=EditEmbedContent.updated_role_rules_embed_field_previous_roles_value(
                before_roles_mentions_content=before_roles_mentions_content),
            inline=False,
        )
        this_embed.add_field(
            name=EditEmbedContent.updated_role_rules_embed_field_new_roles_name(),
            value=EditEmbedContent.updated_role_rules_embed_field_new_roles_value(
                after_roles_mentions_content=after_roles_mentions_content),
            inline=False,
        )

        return this_embed

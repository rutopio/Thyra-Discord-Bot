import discord

from contents.embed.remove import RemoveEmbedContent
from constants.enum.key_type import KEY_TYPE
from constants.constants import CONSTANT


class RemoveEmbed():

    def get_removing_key_embed(key_name, role_message, key_type=None):
        this_embed = discord.Embed(
            title=RemoveEmbedContent.removing_key_embed_title(key_name=key_name),
            description=RemoveEmbedContent.removing_key_embed_description(role_message=role_message),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=RemoveEmbedContent.removing_key_embed_field_note_name(),
            value=RemoveEmbedContent.removing_key_embed_field_note_value(),
            inline=False,
        )
        if key_type == KEY_TYPE.PROTECTED_KEY:
            this_embed.add_field(
                name=RemoveEmbedContent.removing_key_embed_field_about_otp_name(),
                value=RemoveEmbedContent.removing_key_embed_field_about_otp_value(),
                inline=False,
            )
        return this_embed

    def get_removing_all_check_embed():
        this_embed = discord.Embed(
            title=RemoveEmbedContent.removing_all_check_embed_title(),
            description=RemoveEmbedContent.removing_all_check_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=RemoveEmbedContent.removing_all_check_embed_field_note_name(),
            value=RemoveEmbedContent.removing_all_check_embed_field_note_value(),
            inline=False,
        )
        return this_embed

    def get_removed_key_embed(key_name):
        this_embed = discord.Embed(
            title=RemoveEmbedContent.removed_key_embed_title(key_name=key_name),
            description=RemoveEmbedContent.removed_key_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_removed_all_embed():
        this_embed = discord.Embed(
            title=RemoveEmbedContent.removed_all_embed_title(),
            description=RemoveEmbedContent.removed_all_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

import discord

from content.embed.create import CreateEmbedContent
from constant.constants import CONSTANT


class CreateEmbed():

    def get_creating_embed(key_name, type_description):
        this_embed = discord.Embed(
            title=CreateEmbedContent.creating_embed_title(key_name=key_name),
            description=CreateEmbedContent.creating_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=CreateEmbedContent.creating_embed_field_key_type_name(),
            value=CreateEmbedContent.creating_embed_field_key_type_value(type_description=type_description),
            inline=False,
        )
        this_embed.add_field(
            name=CreateEmbedContent.creating_embed_field_note_name(),
            value=CreateEmbedContent.creating_embed_field_note_value(),
            inline=False,
        )
        return this_embed

    def get_created_embed(key_name, type_description, added_roles_content, remove_roles_content, user_name):
        this_embed = discord.Embed(
            title=CreateEmbedContent.created_embed_title(key_name=key_name),
            description=CreateEmbedContent.created_embed_description(key_name=key_name),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=CreateEmbedContent.created_embed_field_key_type_name(),
            value=CreateEmbedContent.created_embed_field_key_type_value(type_description=type_description),
            inline=False,
        )
        this_embed.add_field(
            name=CreateEmbedContent.created_embed_field_assign_roles_name(),
            value=CreateEmbedContent.created_embed_field_assign_roles_value(added_roles_content=added_roles_content),
            inline=False,
        )
        this_embed.add_field(
            name=CreateEmbedContent.created_embed_field_remove_roles_name(),
            value=CreateEmbedContent.created_embed_field_remove_roles_value(remove_roles_content=remove_roles_content),
            inline=False,
        )
        return this_embed

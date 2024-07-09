import os
import datetime
from dotenv import load_dotenv

import discord

from constant.constants import CONSTANT
from constant.db.guild_info import DB_GUILD_INFO
from constant.db.log_info import DB_LOG_INFO
from content.embed.set import SetEmbedContent
from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils.times import TimeUtils

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class SetEmbed():

    def get_welcome_embed_after_verify(guild, user, key_name, added_roles_mentions, remove_roles_mentions):
        # welcome_message = f'- Your new roles: {", ".join(added_roles_mentions)}' if added_roles_mentions else ''

        this_embed = discord.Embed(
            title=SetEmbedContent.welcome_embed_after_verify_title(),
            description=SetEmbedContent.welcome_embed_after_verify_description(
                added_roles_mentions=added_roles_mentions),
            color=CONSTANT.EMBED_COLOR,
        )
        LogUtils.log_to_json(
            log_type=DB_LOG_INFO.USER,
            record={
                DB_LOG_INFO.USER__NAME: user.name,
                DB_LOG_INFO.USER__ID: user.id,
                DB_LOG_INFO.USER__GUILD_NAME: guild.id,
                DB_LOG_INFO.USER__GUILD_ID: guild.id,
                DB_LOG_INFO.USER__KEY: key_name,
            },
        )
        return this_embed

    def get_invalid_key_or_pin_embed(user):
        this_embed = discord.Embed(
            title=SetEmbedContent.invalid_key_or_pin_embed_title(),
            description=SetEmbedContent.invalid_key_or_pin_embed_description(user=user),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=SetEmbedContent.invalid_key_or_pin_embed_field_reasons_name(),
            value=SetEmbedContent.invalid_key_or_pin_embed_field_reasons_value(),
            inline=False,
        )
        return this_embed

    def get_hi_there_embed():
        this_embed = discord.Embed(
            title=SetEmbedContent.hi_there_embed_title(),
            description=SetEmbedContent.hi_there_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )

        this_embed.set_footer(text=SetEmbedContent.hi_there_embed_footer())
        return this_embed

    def get_verification_channel_updated_embed(channel_mention, user_name):
        return discord.Embed(
            title=SetEmbedContent.verification_channel_updated_embed_title(),
            description=SetEmbedContent.verification_channel_updated_embed_description(channel_mention=channel_mention),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_dashboard_channel_updated_embed(channel_mention, user_name):
        return discord.Embed(
            title=SetEmbedContent.dashboard_channel_updated_embed_title(),
            description=SetEmbedContent.dashboard_channel_updated_embed_description(channel_mention=channel_mention),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_dashboard_channel_setting_embed():
        this_embed = discord.Embed(
            title=SetEmbedContent.dashboard_channel_setting_embed_title(),
            description=SetEmbedContent.dashboard_channel_setting_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=SetEmbedContent.dashboard_channel_setting_embed_field_note_name(),
            value=SetEmbedContent.dashboard_channel_setting_embed_field_note_value(),
            inline=False,
        )
        return this_embed

    def get_verification_channel_setting_embed():
        this_embed = discord.Embed(
            title=SetEmbedContent.verification_channel_setting_embed_title(),
            description=SetEmbedContent.verification_channel_setting_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=SetEmbedContent.verification_channel_setting_embed_field_note_name(),
            value=SetEmbedContent.verification_channel_setting_embed_field_note_value(),
            inline=False,
        )
        return this_embed

    def get_user_used_key_before_embed():
        return discord.Embed(
            title=SetEmbedContent.user_used_key_before_embed_title(),
            description=SetEmbedContent.user_used_key_before_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_invalid_timezone_embed(value):
        return discord.Embed(
            title=SetEmbedContent.invalid_timezone_embed_title(),
            description=SetEmbedContent.invalid_timezone_embed_description(value=value),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_valid_timezone_embed(guild, timezone):
        guild_id = guild.id
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            data_to_insert=str(timezone),
            sub_keys=[DB_GUILD_INFO.TIMEZONE],
        )
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        localtime = TimeUtils.convert_to_local_timestamp(guild=guild, utc_timestamp=current_timestamp)

        this_embed = discord.Embed(
            title=SetEmbedContent.valid_timezone_embed_title(),
            description=SetEmbedContent.valid_timezone_embed_description(timezone=timezone, localtime=localtime),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

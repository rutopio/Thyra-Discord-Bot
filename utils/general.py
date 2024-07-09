import os
import datetime
import random
from io import StringIO
from dotenv import load_dotenv
from fuzzywuzzy import process

import discord

from constant.constants import CONSTANT
from constant.db.guild_info import DB_GUILD_INFO
from constant.db.key_info import DB_KEY_INFO
from constant.db.log_info import DB_LOG_INFO
from constant.enum.context_type import CONTEXT_TYPE
from constant.enum.key_type import KEY_TYPE
from content.embed.general import GeneralEmbedContent
from embed.bot import BotEmbed
from utils.key import KeyUtils
from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


def escape_html(string):
    return str(string).replace('&', '＆').replace('>', '＞').replace('<', '＜').replace('\'', '＼').replace('"', '“')


def encode_text(string):
    return string.replace(' ', '-')


def escape_text(string):
    return string.replace('.', '\.').replace('"', '\"').replace("'", "\'")


def get_plural(noun, number):
    return f'{noun}{"s"[:int(number)^1]}'


def generate_pins_by_seed(seed, quantity=50, digits=6):
    random.seed(seed)
    allowed_characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789')
    one_time_pins = [''.join(random.choice(allowed_characters) for _ in range(digits)) for _ in range(quantity)]
    return one_time_pins


# Checks if the user in the passed context is admin
def is_admin(ctx, member=None):
    member = ctx.user if not member else member
    if hasattr(ctx.channel, 'permissions_for'):
        return ctx.channel.permissions_for(member).administrator
    return member.permissions_in(ctx.channel).administrator


# Auto-replies if the user doesn't have admin permission
async def is_admin_reply(
        bot,
        ctx,
        member=None,
        message=GeneralEmbedContent.no_permission_response(),
        message_when=False,
):
    user_is_admin = is_admin(ctx, member)
    if user_is_admin == message_when:
        await ctx.response.send_message(message, ephemeral=True)
    return user_is_admin


def generate_attachment_from_list(pin_list, file_name):
    full_pins = '\n'.join(pin_list)
    buffer = StringIO(full_pins)
    code_attachment = discord.File(buffer, filename=f'{file_name}.csv')
    return code_attachment


async def get_announcement_by_id(guild, details):
    channel_id = details[DB_GUILD_INFO.DASHBOARD_CH__ID]
    announcement_id = details[DB_GUILD_INFO.DASHBOARD_CH__ANNOUNCEMENT_ID]
    channel = guild.get_channel(int(channel_id))
    if channel:
        announcement = await channel.fetch_message(int(announcement_id))
        if announcement:
            return announcement
    return None


def truncate_text(
    text,
    content_type=CONTEXT_TYPE.FIXED,
    buffer_text=CONSTANT.COLLAPSIBLE_CONTENT,
    truncate_back=True,
):
    buffer_length = len(buffer_text)
    max_length = int(content_type.value)
    if len(text) >= max_length - buffer_length:
        if truncate_back:  # truncate from the last
            text = text[:max_length - buffer_length]
        else:  # truncate from the first
            text = text[len(text) - max_length + buffer_length:]
        text += buffer_text

    return text


async def key_name_autocomplete(ctx: discord.AutocompleteContext):
    good_matches = []
    if general.is_admin(ctx=ctx.interaction):
        keys_list = KeyUtils.get_all_keys_name_list(guild=ctx.interaction.guild)
        if ctx.value:
            matches = process.extract(ctx.value, keys_list, limit=25)
            for item in matches:
                # filter the terms which similarity over 40
                if int(item[1]) > 40:
                    good_matches.append(item[0])
        else:
            good_matches = keys_list[:min(len(keys_list), 25)]
    return good_matches


async def protected_keys_auto_complete(ctx: discord.AutocompleteContext):
    good_matches = []

    if general.is_admin(ctx=ctx.interaction):
        keys_list = [
            key[DB_KEY_INFO.NAME] for key in KeyUtils.get_key_infos(guild=ctx.interaction.guild)
            if key[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY
        ]
        if ctx.value:
            matches = process.extract(ctx.value, keys_list, limit=25)
            for item in matches:
                # filter the terms which similarity over 40
                if int(item[1]) > 40:
                    good_matches.append(item[0])
        else:
            good_matches = keys_list[:min(len(keys_list), 25)]
    return good_matches


async def initialize_for_guild(guild):
    try:
        permission_overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
        new_channel = await guild.create_text_channel(CONSTANT.DEFAULT_DASHBOARD_CH_NAME,
                                                      overwrites=permission_overwrites)
        new_channel_id = new_channel.id
        record_info = {
            DB_GUILD_INFO.ID: guild.id,
            DB_GUILD_INFO.NAME: guild.name,
            DB_GUILD_INFO.BOT_JOINED_AT: datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            DB_GUILD_INFO.TIMEZONE: '+0000',
            DB_GUILD_INFO.DASHBOARD_CH: {},
            DB_GUILD_INFO.VERIFICATION_CH: {},
            DB_GUILD_INFO.KEYS_UID: {},
            DB_GUILD_INFO.KEYS_INFO: {},
        }

        query_key = {DB_GUILD_INFO.ID: guild.id}
        MongoDBUtils.update_to_database(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            data_to_insert=record_info,
            query_key=query_key,
        )

        tutorial_embed = BotEmbed.get_bot_tutorial_embed()
        logs_embed = BotEmbed.get_bot_log_embed(guild=guild)
        dashboard_embed = await BotEmbed.get_bot_dashboard_embed(guild=guild)

        announcement = await new_channel.send(embeds=[tutorial_embed, logs_embed, dashboard_embed])
        announcement_id = announcement.id

        dashboard_record = {
            DB_GUILD_INFO.DASHBOARD_CH__ID(new_channel_id),
            DB_GUILD_INFO.DASHBOARD_CH__ANNOUNCEMENT_ID(announcement_id),
        }

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild.id,
            data_to_insert=dashboard_record,
            sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
        )
    except:
        LogUtils.log_to_json(
            log_type=DB_LOG_INFO.STATUS,
            record={
                DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_INITIALIZED,
                DB_LOG_INFO.STATUS__GUILD_NAME: guild.name,
                DB_LOG_INFO.STATUS__GUILD_ID: guild.id
            },
        )


async def update_server_dashboard(guild):
    guild_id = guild.id
    dashboard = MongoDBUtils.query_by_keys(
        db_name=DATABASE_NAME,
        collection_name=GUILD_COLLECTION_NAME,
        query_key=DB_GUILD_INFO.ID,
        query_val=guild_id,
        sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
    )

    is_existed = False
    try:
        if dashboard:
            announcement_message = await general.get_announcement_by_id(guild, dashboard)
            if announcement_message:
                tutorial_embed = BotEmbed.get_bot_tutorial_embed()
                log_embed = BotEmbed.get_bot_log_embed(guild)
                status_embed = await BotEmbed.get_bot_dashboard_embed(guild)
                is_existed = True
                await announcement_message.edit(embeds=[tutorial_embed, log_embed, status_embed])
        if not is_existed:
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=guild_id,
                data_to_insert={},
                sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
            )
    except:
        LogUtils.log_to_json(
            log_type=DB_LOG_INFO.STATUS,
            record={
                DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_DASHBOARD_UPDATE_ERROR,
                DB_LOG_INFO.STATUS__GUILD_NAME: guild.name,
                DB_LOG_INFO.STATUS__GUILD_ID: guild.id
            },
        )

import os
import datetime
from dotenv import load_dotenv

import discord

from constant.constants import CONSTANT
from constant.db.key_info import DB_KEY_INFO
from constant.db.guild_info import DB_GUILD_INFO
from constant.db.user_info import DB_USER_INFO
from content.embed.detail import DetailEmbedContent
from utils.key import KeyUtils
from utils.mongodb import MongoDBUtils
from utils.times import TimeUtils
from utils.user import UserUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')
USER_COLLECTION_NAME = os.getenv('USER_COLLECTION_NAME')


class DetailEmbed():

    def get_key_details_embed(ctx, key_info):
        key_name, key_basic_info, history_log = KeyUtils.get_key_info_content(
            ctx=ctx,
            key_info=key_info,
            show_history=True,
        )
        this_embed = discord.Embed(
            title=DetailEmbedContent.key_details_embed_title(key_name=key_name),
            description=DetailEmbedContent.key_details_embed_description(key_basic_info=key_basic_info),
            color=CONSTANT.EMBED_COLOR,
        )

        if history_log:
            this_embed.add_field(
                name=DetailEmbedContent.key_details_embed_field_edited_history_name(),
                value=DetailEmbedContent.key_details_embed_field_edited_history_value(history_log=history_log),
                inline=False,
            )
        return this_embed

    def get_invalid_user_id_embed(member_id):
        this_embed = discord.Embed(
            title=DetailEmbedContent.invalid_user_id_embed_title(),
            description=DetailEmbedContent.invalid_user_id_embed_description(member_id=member_id),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_key_type_not_protected_embed(key_name):
        this_embed = discord.Embed(
            title=DetailEmbedContent.key_type_not_protected_embed_title(key_name=key_name),
            description=DetailEmbedContent.key_type_not_protected_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_pin_related_key_embed(ctx, key_info, pin_code):
        key_name = key_info[DB_KEY_INFO.NAME]
        if pin_code in key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__USED].keys():
            use_member_id = int(key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__USED][pin_code])
            this_embed = DetailEmbed.get_user_details_embed(ctx, use_member_id)
            this_embed.title = DetailEmbedContent.pin_related_key_embed_used_title(
                key_name=key_name,
                pin_code=pin_code,
            )
        elif pin_code in key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__UNUSED]:
            this_embed = discord.Embed(
                title=DetailEmbedContent.pin_related_key_embed_unused_title(
                    key_name=key_name,
                    pin_code=pin_code,
                ),
                description=DetailEmbedContent.pin_related_key_embed_unused_description(),
                color=CONSTANT.EMBED_COLOR,
            )
        else:
            this_embed = discord.Embed(
                title=DetailEmbedContent.pin_related_key_embed_invalid_title(
                    key_name=key_name,
                    pin_code=pin_code,
                ),
                description=DetailEmbedContent.pin_related_key_embed_invalid_description(),
                color=CONSTANT.EMBED_COLOR,
            )
        return this_embed

    @staticmethod
    def get_user_details_embed(ctx, member_id):
        guild_id = ctx.guild_id
        now_time = datetime.datetime.now(tz=datetime.timezone.utc)
        member_id = int(member_id)

        member_info = UserUtils.get_guild_member_info_by_user_id(guild=ctx.guild, user_id=member_id)
        if not member_info:
            this_embed = get_invalid_user_id_embed(member_id=member_id)
            return this_embed

        member_mention = ctx.guild.get_member(member_id).mention
        timedelta_between_today_and_joined_at = (now_time - member_info['joined_at']).days
        timedelta_between_today_and_created_at = (now_time - member_info['created_at']).days

        user_roles = member_info['roles']
        num_role_shows = 10
        is_truncated = True if len(user_roles) > num_role_shows else False
        if is_truncated:
            roles_content = ', '.join(user_roles[:num_role_shows]) if user_roles else '-'
            roles_content += f' (+{len(user_roles)-num_role_shows} more)'
        else:
            roles_content = ', '.join(user_roles) if user_roles else '-'

        user_info_content = f'''
    `[    User Id ]` {member_info['id']}
    `[    Mention ]` {member_mention}
    `[  Own Roles ]` {roles_content}
    `[   Top Role ]` {member_info['top_role']}
    `[ Created At ]` {TimeUtils.convert_to_local_timestamp(guild=ctx.guild, utc_timestamp=member_info['created_at'].timestamp()).strftime(CONSTANT.DATE_FORMAT)} ({timedelta_between_today_and_created_at} {general.get_plural('day', timedelta_between_today_and_created_at)} ago)
    `[  Joined At ]` {TimeUtils.convert_to_local_timestamp(guild=ctx.guild, utc_timestamp=member_info['joined_at'].timestamp()).strftime(CONSTANT.DATE_FORMAT)} ({timedelta_between_today_and_joined_at} {general.get_plural('day', timedelta_between_today_and_joined_at)} ago)
        '''

        user_used_identifier_in_this_guild = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=USER_COLLECTION_NAME,
            query_key=DB_USER_INFO.USER_ID,
            query_val=int(member_id),
            sub_keys=[DB_USER_INFO.USED_KEYS, str(guild_id)],
        )

        identifiers_and_key_infos = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO],
        )

        user_used_key_name = []

        for key_identifier, key_name in identifiers_and_key_infos.items():
            if key_identifier in user_used_identifier_in_this_guild:
                user_used_key_name.append(key_name)

        this_embed = discord.Embed(
            title=DetailEmbedContent.user_details_embed_title(username=member_info['display_name']),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.set_thumbnail(url=member_info['display_avatar'])

        if user_used_key_name:
            key_content = ''
            sorted_user_used_key_name = sorted(user_used_key_name,
                                               key=lambda x: x[DB_KEY_INFO.USED_MEMBERS].get(str(member_id), {}).get(
                                                   DB_KEY_INFO.USED_MEMBERS__TIMESTAMP, datetime))

            for key_name in sorted_user_used_key_name:
                key_content += KeyUtils.get_used_key_with_orders(
                    ctx=ctx,
                    key=key_name,
                    user_data=member_info,
                    member_id=member_id,
                )

            this_embed.description = DetailEmbedContent.user_details_embed_description(key_content=key_content)

            this_embed.add_field(
                name=DetailEmbedContent.user_details_embed_field_note_name(),
                value=DetailEmbedContent.user_details_embed_field_note_value(),
                inline=False,
            )

        this_embed.add_field(
            name=DetailEmbedContent.user_details_embed_field_member_info_name(),
            value=DetailEmbedContent.user_details_embed_field_member_info_value(user_info_content=user_info_content),
            inline=False,
        )

        return this_embed

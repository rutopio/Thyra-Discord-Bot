import os
import discord
import datetime
import pytz
from dotenv import load_dotenv

from content.utils.key import KeyUtilsContent
from content.embed.bot import BotEmbedContent

from embed.general import GeneralEmbed

from constant.usage_limits import USAGE_LIMIT
from constant.enum.key_type import KEY_TYPE
from constant.constants import CONSTANT
from constant.db.key_info import DB_KEY_INFO
from constant.db.guild_info import DB_GUILD_INFO
from constant.key_type_name import KEY_TYPE_NAME
from constant.edit_operation import EDIT_OPERATION

from utils.times import TimeUtils
from utils.role import RoleUtils
from utils.mongodb import MongoDBUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class KeyUtils():

    @staticmethod
    def get_key_identifier_by_timestamp(timestamp):
        return str(int(timestamp * 10000))

    @staticmethod
    def get_identifier_and_name_dict(guild):
        guild_id = guild.id
        return MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_UID],
        )

    @staticmethod
    def get_name_and_identifier_dict(guild):
        id_name_relationship = KeyUtils.get_identifier_and_name_dict(guild=guild)
        return {key_name: identifier for identifier, key_name in id_name_relationship.items()}

    @staticmethod
    def get_all_keys_name_list(guild):
        guild_id = guild.id
        return list(
            MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=guild_id,
                sub_keys=[DB_GUILD_INFO.KEYS_UID],
            ).values())

    @staticmethod
    def get_key_infos(guild):
        guild_id = guild.id
        return MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO],
        ).values()

    @staticmethod
    def get_key_info_by_identifier(guild, identifier):
        guild_id = guild.id
        return MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier],
        )

    @staticmethod
    def get_key_info_by_name(guild, key_name):
        name_id_relationship = KeyUtils.get_name_and_identifier_dict(guild)
        if key_name in name_id_relationship:
            key_identifier = name_id_relationship[key_name]
            return KeyUtils.get_key_info_by_identifier(guild=guild, identifier=key_identifier)
        return None

    @staticmethod
    def is_same_name_key_exists(guild, new_key_name):
        guild_id = guild.id
        key_names = KeyUtils.get_all_keys_name_list(guild)
        if new_key_name in key_names:
            return True
        else:
            return False

    @staticmethod
    async def callback_if_key_name_too_long(ctx, key_name):
        if len(key_name) > USAGE_LIMIT.MAX_LENGTH_OF_KEY_NAME():
            too_long_embed = GeneralEmbed.get_name_too_long_embed(key_name=key_name)
            await ctx.response.send_message(embed=too_long_embed, ephemeral=True)
            return True
        else:
            return False

    @staticmethod
    async def callback_if_key_out_of_quota(ctx, key_type):
        num_of_type_keys = 0
        for key_info in KeyUtils.get_key_infos(ctx.guild):
            if key_info[DB_KEY_INFO.TYPE] == key_type:
                num_of_type_keys += 1

        if num_of_type_keys >= USAGE_LIMIT.MAX_NUMBER_OF_KEY_PER_TYPE():
            key_num_out_of_quota_embed = GeneralEmbed.get_key_is_full_embed()
            await ctx.response.send_message(embed=key_num_out_of_quota_embed, ephemeral=True)
            return True
        else:
            return False

    @staticmethod
    async def callback_usage_limit_number_invalid(ctx, number):
        if number < 0:
            invalid_number_embed = GeneralEmbed.get_invalid_usage_limit_embed()
            await ctx.response.send_message(embed=invalid_number_embed, ephemeral=True)
            return True

        if number > USAGE_LIMIT.MAX_NUMBER_OF_KEY_USAGE_LIMIT():
            usage_limit_out_of_quota_embed = GeneralEmbed.get_usage_limit_too_many_embed(number=number)
            await ctx.response.send_message(embed=usage_limit_out_of_quota_embed, ephemeral=True)
            return True
        else:
            return False

    @staticmethod
    async def callback_if_otp_number_invalid(ctx, num_otp):
        if num_otp < 0:
            invalid_number_embed = GeneralEmbed.get_invalid_otp_number_embed(value=num_otp)
            await ctx.response.send_message(embed=invalid_number_embed, ephemeral=True)
            return True

        if num_otp > USAGE_LIMIT.MAX_NUMBER_OF_PINS():
            otp_num_out_of_quota_embed = GeneralEmbed.get_otp_too_many_embed(number=num_otp)
            await ctx.response.send_message(embed=otp_num_out_of_quota_embed, ephemeral=True)
            return True
        else:
            return False

    @staticmethod
    async def callback_if_key_name_exists(ctx, key_name):
        if KeyUtils.is_same_name_key_exists(ctx.guild, key_name):
            same_key_name_exist_embed = GeneralEmbed.get_same_key_name_exist_embed(key_name)
            await ctx.response.send_message(embed=same_key_name_exist_embed, ephemeral=True)
            return True
        else:
            return False

    @staticmethod
    def get_key_edited_history(ctx, key_info, allow_truncated=True):

        history = {
            'name_history': [key_info[DB_KEY_INFO.NAME]],
            'active_history': [key_info[DB_KEY_INFO.STATUS]],
            'counts_history': [key_info[DB_KEY_INFO.COUNT]],
            'assign_history': [key_info[DB_KEY_INFO.ASSIGN_ROLES]],
            'remove_history': [key_info[DB_KEY_INFO.REMOVE_ROLES]],
        }
        edited_history = [
            key_info[DB_KEY_INFO.EDITED][key] for key in sorted(key_info[DB_KEY_INFO.EDITED], reverse=True)
        ]
        log_string = ''

        if allow_truncated:
            num_truncated = 5
            is_truncated = True if len(edited_history) > num_truncated else False
            edited_history = edited_history[max(-num_truncated, -len(edited_history)):]

        for log in edited_history:
            edit_at_time = TimeUtils.convert_to_local_timestamp(ctx.guild, log[DB_KEY_INFO.EDITED__AT]).strftime(
                CONSTANT.DATE_FORMAT)

            if ctx.guild.get_member(int(log[DB_KEY_INFO.EDITED__USER_ID])):
                editor_mention = ctx.guild.get_member(int(log[DB_KEY_INFO.EDITED__USER_ID])).mention
            else:
                editor_mention = KeyUtilsContent.left_member_string

            log_string += f'- `{edit_at_time}` · {editor_mention}\n'

            event = log[DB_KEY_INFO.EDITED__EVENT]

            if event == EDIT_OPERATION.RENAME:
                history['name_history'].append(log[DB_KEY_INFO.EDITED__PREVIOUS_VALUE])
                log_string += KeyUtilsContent.rename_log(history['name_history'][1], history['name_history'][0])
                history['name_history'].pop(0)
            elif event == EDIT_OPERATION.UPDATE_STATUS:
                history['active_history'].append(log[DB_KEY_INFO.EDITED__PREVIOUS_VALUE])
                status1 = KeyUtilsContent.active_string if history['active_history'][
                    1] else KeyUtilsContent.inactive_string
                status2 = KeyUtilsContent.active_string if history['active_history'][
                    0] else KeyUtilsContent.inactive_string
                log_string += KeyUtilsContent.UPDATE_STATUS_log(status1, status2)
                history['active_history'].pop(0)
            elif event == EDIT_OPERATION.UPDATE_USAGE_COUNT:
                history['counts_history'].append(log[DB_KEY_INFO.EDITED__PREVIOUS_VALUE])
                if key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.LIMITED_KEY:
                    log_string += KeyUtilsContent.adjust_times_log(
                        history['counts_history'][1],
                        history['counts_history'][0],
                    )
                elif key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY:
                    log_string += KeyUtilsContent.gen_more_otps_log(history['counts_history'][1])
                history['counts_history'].pop(0)
            elif event == EDIT_OPERATION.UPDATE_ASSIGN_ROLES:
                num_role_shows = 2
                history['assign_history'].append(log[DB_KEY_INFO.EDITED__PREVIOUS_VALUE])
                pre_roles = RoleUtils.get_roles_mention_list(ctx, history['assign_history'][1])

                is_pre_truncated = True if len(pre_roles) > num_role_shows else False
                if is_pre_truncated:
                    pre_roles_string = KeyUtilsContent.separator.join(
                        pre_roles[:num_role_shows]) if pre_roles else KeyUtilsContent.none_mark
                    pre_roles_string += KeyUtilsContent.omit_more(len(pre_roles), num_role_shows)
                else:
                    pre_roles_string = KeyUtilsContent.separator.join(
                        pre_roles) if pre_roles else KeyUtilsContent.none_mark

                now_roles = RoleUtils.get_roles_mention_list(ctx, history['assign_history'][0])
                is_now_truncated = True if len(now_roles) > num_role_shows else False
                if is_now_truncated:
                    now_roles_string = KeyUtilsContent.separator.join(
                        now_roles[:num_role_shows]) if now_roles else KeyUtilsContent.none_mark
                    now_roles_string += KeyUtilsContent.omit_more(len(now_roles), num_role_shows)
                else:
                    now_roles_string = KeyUtilsContent.separator.join(
                        now_roles) if now_roles else KeyUtilsContent.none_mark

                log_string += KeyUtilsContent.EDIT_ASSIGN_ROLES_roles_log(pre_roles_string, now_roles_string)
                history['assign_history'].pop(0)
            elif event == EDIT_OPERATION.UPDATE_REMOVE_ROLES:
                num_role_shows = 2
                history['remove_history'].append(log[DB_KEY_INFO.EDITED__PREVIOUS_VALUE])
                pre_roles = RoleUtils.get_roles_mention_list(ctx, history['remove_history'][1])

                is_pre_truncated = True if len(pre_roles) > num_role_shows else False
                if is_pre_truncated:
                    pre_roles_string = KeyUtilsContent.separator.join(
                        pre_roles[:num_role_shows]) if pre_roles else KeyUtilsContent.none_mark
                    pre_roles_string += KeyUtilsContent.omit_more(len(pre_roles), num_role_shows)
                else:
                    pre_roles_string = KeyUtilsContent.separator.join(
                        pre_roles) if pre_roles else KeyUtilsContent.none_mark

                now_roles = RoleUtils.get_roles_mention_list(ctx, history['remove_history'][0])
                is_now_truncated = True if len(now_roles) > num_role_shows else False
                if is_now_truncated:
                    now_roles_string = KeyUtilsContent.separator.join(
                        now_roles[:num_role_shows]) if now_roles else KeyUtilsContent.none_mark
                    now_roles_string += KeyUtilsContent.omit_more(len(now_roles), num_role_shows)
                else:
                    now_roles_string = KeyUtilsContent.separator.join(
                        now_roles) if now_roles else KeyUtilsContent.none_mark

                log_string += KeyUtilsContent.EDIT_REMOVE_ROLES_roles_log(pre_roles_string, now_roles_string)
                history['remove_history'].pop(0)

        return log_string

    @staticmethod
    def get_key_info_content(ctx, key_info, show_history=False, show_status=True, show_type=True):
        key_name = key_info[DB_KEY_INFO.NAME]
        key_types_dict = {
            KEY_TYPE.REGULAR_KEY: KEY_TYPE_NAME.REGULAR_KEY_WITH_EMOJI,
            KEY_TYPE.LIMITED_KEY: KEY_TYPE_NAME.LIMITED_KEY_WITH_EMOJI,
            KEY_TYPE.PROTECTED_KEY: KEY_TYPE_NAME.PROTECTED_KEY_WITH_EMOJI,
        }
        key_type = key_types_dict[key_info[DB_KEY_INFO.TYPE]]

        added_roles_mentions = RoleUtils.get_roles_mention_list(ctx, key_info[DB_KEY_INFO.ASSIGN_ROLES])
        remove_roles_mentions = RoleUtils.get_roles_mention_list(ctx, key_info[DB_KEY_INFO.REMOVE_ROLES])

        if key_info[DB_KEY_INFO.COUNT] > 0:
            member_counts = f'{len(key_info[DB_KEY_INFO.USED_MEMBERS])} / {key_info[DB_KEY_INFO.COUNT]}'
        else:
            member_counts = f'{len(key_info[DB_KEY_INFO.USED_MEMBERS])}'

        added_roles_content = KeyUtilsContent.separator.join(
            added_roles_mentions) if added_roles_mentions else KeyUtilsContent.none_mark
        remove_roles_content = KeyUtilsContent.separator.join(
            remove_roles_mentions) if remove_roles_mentions else KeyUtilsContent.none_mark
        current_status = f'{KeyUtilsContent.active_emoji} {KeyUtilsContent.active_string}' if key_info[
            DB_KEY_INFO.STATUS] else f'{KeyUtilsContent.inactive_emoji} {KeyUtilsContent.inactive_string}'
        info_content = ''

        if show_status:
            info_content += KeyUtilsContent.key_info_status(current_status=current_status)
        else:
            key_name = f'{KeyUtilsContent.active_emoji} {key_info[DB_KEY_INFO.NAME]}' if key_info[
                DB_KEY_INFO.STATUS] else f'{KeyUtilsContent.inactive_emoji} {key_info[DB_KEY_INFO.NAME]}'

        if show_type:
            info_content += KeyUtilsContent.key_info_type(key_type=key_type)

        info_content += KeyUtilsContent.key_info_content(
            added_roles_content=added_roles_content,
            remove_roles_content=remove_roles_content,
            member_counts=member_counts,
        )

        if ctx.guild.get_member(int(key_info[DB_KEY_INFO.CREATOR_ID])):
            creator_mention = ctx.guild.get_member(int(key_info[DB_KEY_INFO.CREATOR_ID])).mention
        else:
            creator_mention = KeyUtilsContent.left_member_string

        create_at_time = TimeUtils.convert_to_local_timestamp(guild=ctx.guild,
                                                              utc_timestamp=key_info[DB_KEY_INFO.CREATED_AT]).strftime(
                                                                  CONSTANT.DATE_FORMAT)
        info_content += KeyUtilsContent.key_info_creator(
            create_at_time=create_at_time,
            creator_mention=creator_mention,
        )

        if show_history:
            return key_name, info_content, KeyUtils.get_key_edited_history(ctx, key_info)
        else:
            return key_name, info_content, None

    @staticmethod
    def get_used_key_with_orders(ctx, key, user_data, member_id):
        user_details_in_key = key[DB_KEY_INFO.USED_MEMBERS][str(member_id)]
        max_count = key[DB_KEY_INFO.COUNT] if key[DB_KEY_INFO.COUNT] > 0 else KeyUtilsContent.inf_mark

        user_joined_guild_datetime = user_data['joined_at'].replace(tzinfo=pytz.timezone('UTC'))
        user_used_key_datetime = datetime.datetime.fromtimestamp(
            user_details_in_key[DB_KEY_INFO.USED_MEMBERS__TIMESTAMP]).replace(tzinfo=pytz.timezone('UTC'))

        time_between_joined_and_use_key = TimeUtils.get_timedelta_between_joined_and_use_key(
            user_joined_guild_datetime, user_used_key_datetime)
        if key[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY:
            return KeyUtilsContent.used_key_order_protected(
                key_name=key[DB_KEY_INFO.NAME],
                used_at=TimeUtils.convert_to_local_timestamp(
                    ctx.guild, user_details_in_key[DB_KEY_INFO.USED_MEMBERS__TIMESTAMP]).strftime(CONSTANT.DATE_FORMAT),
                time_passed=time_between_joined_and_use_key,
                used_order=
                f'{user_details_in_key[DB_KEY_INFO.USED_MEMBERS__ORDER]} / {len(key[DB_KEY_INFO.USED_MEMBERS])}',
                max_count=max_count,
                used_pin=user_details_in_key[DB_KEY_INFO.USED_MEMBERS__PIN])

        else:
            return KeyUtilsContent.used_key_order(
                key_name=key[DB_KEY_INFO.NAME],
                used_at=TimeUtils.convert_to_local_timestamp(
                    ctx.guild, user_details_in_key[DB_KEY_INFO.USED_MEMBERS__TIMESTAMP]).strftime(CONSTANT.DATE_FORMAT),
                time_passed=time_between_joined_and_use_key,
                max_count=max_count,
                used_order=
                f'{user_details_in_key[DB_KEY_INFO.USED_MEMBERS__ORDER]} / {len(key[DB_KEY_INFO.USED_MEMBERS])}',
            )

    def get_keys_names_status_counts(keys_info):
        key_name_status_count_list = []
        for key_info in keys_info:
            key_name = key_info[DB_KEY_INFO.NAME]
            key_status = BotEmbedContent.active_emoji if key_info[
                DB_KEY_INFO.STATUS] else BotEmbedContent.inactive_emoji
            if key_info[DB_KEY_INFO.COUNT] > 0:
                member_counts = BotEmbedContent.used_users_counter(
                    used_num=len(key_info[DB_KEY_INFO.USED_MEMBERS]),
                    max_num=key_info[DB_KEY_INFO.COUNT],
                )
            else:
                member_counts = BotEmbedContent.used_users_counter(used_num=len(key_info[DB_KEY_INFO.USED_MEMBERS]))
            content = f'- {key_status} | `{key_name}` | `({member_counts})`'
            key_name_status_count_list.append(content)
        return key_name_status_count_list

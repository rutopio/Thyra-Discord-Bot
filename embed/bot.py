import os
import discord
import datetime
from dotenv import load_dotenv

from content.embed.bot import BotEmbedContent

from constant.constants import CONSTANT
from constant.enum.key_type import KEY_TYPE
from constant.guild_operation import GUILD_OPERATION
from constant.db.key_info import DB_KEY_INFO
from constant.db.guild_info import DB_GUILD_INFO

from utils.times import TimeUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class BotEmbed():

    async def get_bot_dashboard_embed(guild):
        key_infos = KeyUtils.get_key_infos(guild=guild)

        regular_key_names = []
        limited_key_names = []
        protected_key_names = []

        for key_info in key_infos:
            key_type = key_info[DB_KEY_INFO.TYPE]
            if key_type == KEY_TYPE.REGULAR_KEY:
                regular_key_names.append(key_info)
            elif key_type == KEY_TYPE.LIMITED_KEY:
                limited_key_names.append(key_info)
            elif key_type == KEY_TYPE.PROTECTED_KEY:
                protected_key_names.append(key_info)

        is_verification_dialog_exist = False
        try:
            if MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=guild.id,
                    sub_keys=[DB_GUILD_INFO.VERIFICATION_CH],
            ):
                current_verification_channel_id = int(
                    MongoDBUtils.query_by_keys(
                        db_name=DATABASE_NAME,
                        collection_name=GUILD_COLLECTION_NAME,
                        query_key=DB_GUILD_INFO.ID,
                        query_val=guild.id,
                        sub_keys=[DB_GUILD_INFO.VERIFICATION_CH, DB_GUILD_INFO.VERIFICATION_CH__ID],
                    ))
                if guild.get_channel(current_verification_channel_id):
                    current_verification_message_id = int(
                        MongoDBUtils.query_by_keys(
                            db_name=DATABASE_NAME,
                            collection_name=GUILD_COLLECTION_NAME,
                            query_key=DB_GUILD_INFO.ID,
                            query_val=guild.id,
                            sub_keys=[DB_GUILD_INFO.VERIFICATION_CH, DB_GUILD_INFO.VERIFICATION_CH__ANNOUNCEMENT_ID],
                        ))

                    msg = await guild.get_channel(current_verification_channel_id).fetch_message(
                        current_verification_message_id)
                    if msg:
                        is_verification_dialog_exist = True
                        current_verification_channel_mention = guild.get_channel(
                            current_verification_channel_id).mention
        except:
            pass

        if not is_verification_dialog_exist:
            current_verification_channel_mention = BotEmbedContent.bot_dashboard_embed_field_verification_ch_if_invalid(
            )

        timezone_offset = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild.id,
            sub_keys=[DB_GUILD_INFO.TIMEZONE],
        )
        this_embed = discord.Embed(
            title=BotEmbedContent.bot_dashboard_embed_title(),
            description=BotEmbedContent.bot_dashboard_embed_description(),
            color=CONSTANT.EMBED_COLOR,
            timestamp=datetime.datetime.now(),
        )

        # Number of Members
        this_embed.add_field(
            name=BotEmbedContent.bot_dashboard_embed_field_num_member_name(),
            value=BotEmbedContent.bot_dashboard_embed_field_num_member_value(guild=guild),
            inline=True,
        )
        # Number of Bots
        this_embed.add_field(
            name=BotEmbedContent.bot_dashboard_embed_field_num_bot_name(),
            value=BotEmbedContent.bot_dashboard_embed_field__num_bot_value(guild=guild),
            inline=True,
        )
        # Number of Roles
        this_embed.add_field(
            name=BotEmbedContent.bot_dashboard_embed_field_num_role_name(),
            value=BotEmbedContent.bot_dashboard_embed_field_num_role_value(guild=guild),
            inline=True,
        )

        # Timezone
        this_embed.add_field(
            name=BotEmbedContent.bot_dashboard_embed_field_timezone_name(),
            value=BotEmbedContent.bot_dashboard_embed_field_timezone_value(timezone_offset=timezone_offset),
            inline=True,
        )
        # Verification Ch.
        this_embed.add_field(
            name=BotEmbedContent.bot_dashboard_embed_field_verification_ch_name(),
            value=current_verification_channel_mention,
            inline=True,
        )
        if regular_key_names:
            this_embed.add_field(
                name=BotEmbedContent.bot_dashboard_embed_field_regular_key_name(regular_key_names=regular_key_names),
                value=BotEmbedContent.bot_dashboard_embed_field_regular_key_value(
                    content='\n'.join(KeyUtils.get_keys_names_status_counts(keys_info=regular_key_names))),
                inline=False,
            )
        if limited_key_names:
            this_embed.add_field(
                name=BotEmbedContent.bot_dashboard_embed_field_limited_key_name(limited_key_names=limited_key_names),
                value=BotEmbedContent.bot_dashboard_embed_field_limited_key_value(
                    content='\n'.join(KeyUtils.get_keys_names_status_counts(keys_info=limited_key_names))),
                inline=False,
            )
        if protected_key_names:
            this_embed.add_field(
                name=BotEmbedContent.bot_dashboard_embed_field_protected_name(protected_key_names=protected_key_names),
                value=BotEmbedContent.bot_dashboard_embed_field_protected_value(
                    content='\n'.join(KeyUtils.get_keys_names_status_counts(keys_info=protected_key_names))),
                inline=False,
            )

        this_embed.set_footer(text=BotEmbedContent.bot_dashboard_embed_footer())
        return this_embed

    def get_bot_log_embed(guild):
        server_logs = list(
            MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=guild.id,
                sub_keys=[DB_GUILD_INFO.LOGS],
            ).values())
        content = ''
        # show latest 15 logs
        for _, log in enumerate(server_logs[-15:]):
            edit_at_time = TimeUtils.convert_to_local_timestamp(
                guild=guild,
                utc_timestamp=log[DB_GUILD_INFO.LOGS__LOGGED_AT],
            ).strftime(CONSTANT.DATE_FORMAT)

            editor = guild.get_member(int(log[DB_GUILD_INFO.LOGS__USER_ID]))
            if editor:
                editor_mention = editor.mention
            else:
                editor_mention = BotEmbedContent.editor_mention_if_user_invalid()

            event = log[DB_GUILD_INFO.LOGS__EVENT]
            details = log[DB_GUILD_INFO.LOGS__DETAILS]

            if event == GUILD_OPERATION.SET_TIMEZONE:
                full_description = BotEmbedContent.set_timezone_string(details=details)
            elif event == GUILD_OPERATION.CREATE_KEY:
                full_description = BotEmbedContent.create_key_string(details=details)
            elif event == GUILD_OPERATION.EDIT_STATUS:
                full_description = BotEmbedContent.edit_status_string(details=details)
            elif event == GUILD_OPERATION.EDIT_NAME:
                full_description = BotEmbedContent.edit_name_string(details=details)
            elif event == GUILD_OPERATION.EDIT_USAGE_COUNT:
                full_description = BotEmbedContent.EDIT_USAGE_COUNT_string(details=details)
            elif event == GUILD_OPERATION.EDIT_GEN_OTP:
                full_description = BotEmbedContent.edit_gen_otp_string(details=details)
            elif event == GUILD_OPERATION.EDIT_ASSIGN_ROLES:
                full_description = BotEmbedContent.EDIT_ASSIGN_ROLES_string(details=details)
            elif event == GUILD_OPERATION.EDIT_REMOVE_ROLES:
                full_description = BotEmbedContent.EDIT_REMOVE_ROLES_string(details=details)
            elif event == GUILD_OPERATION.REMOVE_ALL_KEYS:
                full_description = BotEmbedContent.remove_all_string(details=details)
            elif event == GUILD_OPERATION.REMOVE_KEY:
                full_description = BotEmbedContent.remove_key_string(details=details)
            elif event == GUILD_OPERATION.SET_DASHBOARD_CH:
                full_description = BotEmbedContent.set_dashboard_string(details=details)
            elif event == GUILD_OPERATION.SET_VERIFICATION_CH:
                full_description = BotEmbedContent.set_verification_string(details=details)

            content += f'- `{edit_at_time}` · {editor_mention}\n  - {full_description}\n'

        this_embed = discord.Embed(
            title=BotEmbedContent.bot_log_embed_title(),
            description=BotEmbedContent.bot_log_embed_description(content=content),
            color=CONSTANT.EMBED_COLOR,
        )
        return this_embed

    def get_bot_tutorial_embed():

        this_embed = discord.Embed(
            title=BotEmbedContent.bot_tutorial_embed_title(),
            url=BotEmbedContent.bot_tutorial_embed_url(),
            description=BotEmbedContent.bot_tutorial_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
        this_embed.add_field(
            name=BotEmbedContent.bot_tutorial_embed_field_quick_start_name(),
            value=BotEmbedContent.bot_tutorial_embed_field_quick_start_value(),
            inline=False,
        )
        this_embed.add_field(
            name=BotEmbedContent.bot_tutorial_embed_field_commands_name(),
            value=BotEmbedContent.bot_tutorial_embed_field_commands_value(),
            inline=False,
        )
        # this_embed.add_field(
        #     name='Support & Contact',
        #     value='Please refer to https://thyra.pages.dev , or join our [Support Server](https://discord.gg/B2r8VkgGe2).',
        #     inline=False)

        return this_embed

    def get_dashboard_updated():
        return discord.Embed(
            title=BotEmbedContent.dashboard_updated_embed_title(),
            color=CONSTANT.EMBED_COLOR,
            timestamp=datetime.datetime.now(),
        )

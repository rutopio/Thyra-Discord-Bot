import os
import datetime
import discord
from dotenv import load_dotenv

# from embed import create_embed
from component.general import BasicViewComponent, AssignRoleSelector, RemoveRoleSelector, CancelButton

from contents.view.create import CreateViewContent
from embed.create import CreateEmbed

from constants.enum.key_type import KEY_TYPE
from constants.guild_operation import GUILD_OPERATION
from constants.db.key_info import DB_KEY_INFO
from constants.db.guild_info import DB_GUILD_INFO

from utils.role import RoleUtils
from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class CreateKeyConfirmButton(discord.ui.Button):

    def __init__(self, key_name, assign_roles_selector, remove_roles_selector, key_type, times):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=CreateViewContent.create_key_confirm_button_emoji,
            label=CreateViewContent.create_key_confirm_button_label,
            row=2,
            custom_id=CreateViewContent.create_key_confirm_button_id,
        )
        self.key_name = str(key_name)
        self.assign_roles_selector = assign_roles_selector
        self.remove_roles_selector = remove_roles_selector
        self.key_type = key_type
        self.times = int(times)

    async def callback(self, interaction: discord.Interaction):
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=current_timestamp)

        random_seed = int(interaction.guild_id) + int(current_timestamp * 10000) + 5566
        key_info = {
            DB_KEY_INFO.NAME: self.key_name,
            DB_KEY_INFO.PREVIOUS_NAME: [],
            DB_KEY_INFO.STATUS: True,
            DB_KEY_INFO.TYPE: self.key_type,
            DB_KEY_INFO.COUNT: self.times,
            DB_KEY_INFO.CREATOR_ID: interaction.user.id,
            DB_KEY_INFO.CREATED_AT: current_timestamp,
            DB_KEY_INFO.ASSIGN_ROLES: self.assign_roles_selector.selected_options,
            DB_KEY_INFO.REMOVE_ROLES: self.remove_roles_selector.selected_options,
            DB_KEY_INFO.USED_MEMBERS: {},
            DB_KEY_INFO.EDITED: {},
        }

        added_roles_mentions = RoleUtils.get_roles_mention_list(
            interaction=interaction,
            role_list=key_info[DB_KEY_INFO.ASSIGN_ROLES],
        )
        remove_roles_mentions = RoleUtils.get_roles_mention_list(
            interaction=interaction,
            role_list=key_info[DB_KEY_INFO.REMOVE_ROLES],
        )

        added_roles_content = '\n'.join(['- ' + item for item in added_roles_mentions
                                         ]) if added_roles_mentions else CreateViewContent.none_string
        remove_roles_content = '\n'.join(['- ' + item for item in remove_roles_mentions
                                          ]) if remove_roles_mentions else CreateViewContent.none_string

        if self.key_type == KEY_TYPE.REGULAR_KEY:
            key_type_description = CreateViewContent.regular_key_type_description()
        elif self.key_type == KEY_TYPE.LIMITED_KEY:
            key_type_description = CreateViewContent.limited_key_type_description(times=self.times)
        elif self.key_type == KEY_TYPE.PROTECTED_KEY:
            key_type_description = CreateViewContent.protected_key_type_description(times=self.times)

        this_embed = CreateEmbed.get_created_embed(
            key_name=self.key_name,
            type_description=key_type_description,
            added_roles_content=added_roles_content,
            remove_roles_content=remove_roles_content,
            user_name=interaction.user.name,
        )

        if self.key_type == KEY_TYPE.PROTECTED_KEY:
            one_time_pins_generated_list = general.generate_pins_by_seed(seed=random_seed, quantity=self.times)
            code_attachment = general.generate_attachment_from_list(
                pin_list=one_time_pins_generated_list,
                file_name=CreateViewContent.otp_attachment_name(
                    key_name=self.key_name,
                    times=self.times,
                ),
            )
            this_embed.add_field(
                name=CreateViewContent.otp_attachment_field_title(times=self.times),
                value=CreateViewContent.otp_attachment_field_description(times=self.times),
                inline=False,
            )

            key_info[DB_KEY_INFO.OTPS] = {
                DB_KEY_INFO.OTPS__SEED: random_seed,
                DB_KEY_INFO.OTPS__UNUSED: one_time_pins_generated_list,
                DB_KEY_INFO.OTPS__USED: {},
            }

        await interaction.response.edit_message(view=None, embed=this_embed)

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=key_info,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier],
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=self.key_name,
            sub_keys=[DB_GUILD_INFO.KEYS_UID, identifier],
        )
        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.CREATE_KEY,
            description=[self.key_name, self.key_type],
        )

        if self.key_type == KEY_TYPE.PROTECTED_KEY:
            await interaction.followup.send(
                content=CreateViewContent.otp_attachment_embed_title(
                    key_name=self.key_name,
                    times=self.times,
                ),
                file=code_attachment,
                ephemeral=True,
            )

        await general.update_server_dashboard(guild=interaction.guild)

import discord
import os
from dotenv import load_dotenv

from embed.remove import RemoveEmbed

from contents.view.remove import RemoveViewContent

from constants.guild_operation import GUILD_OPERATION
from constants.db.key_info import DB_KEY_INFO
from constants.db.guild_info import DB_GUILD_INFO

from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class RemoveAllKeysConfirmButton(discord.ui.Button):

    def __init__(self, ctx):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label=RemoveViewContent.remove_all_keys_confirm_button_label,
            emoji=RemoveViewContent.remove_all_keys_confirm_button_emoji,
            row=0,
            custom_id=RemoveViewContent.remove_all_keys_confirm_button_id,
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert={},
            sub_keys=[DB_GUILD_INFO.KEYS_INFO],
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert={},
            sub_keys=[DB_GUILD_INFO.KEYS_UID],
        )
        this_embed = RemoveEmbed.get_removed_all_embed()
        await interaction.response.edit_message(embed=this_embed, view=None, content=None)

        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.REMOVE_ALL_KEYS,
            description='',
        )
        await general.update_server_dashboard(guild=interaction.guild)


class RemoveKeyConfirmButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label=RemoveViewContent.remove_key_confirm_button_label,
            emoji=RemoveViewContent.remove_key_confirm_button_emoji,
            row=0,
            custom_id=RemoveViewContent.remove_key_confirm_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info
        self.key_name = key_info[DB_KEY_INFO.NAME]

    async def callback(self, interaction: discord.Interaction):
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])
        MongoDBUtils.remove_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier],
        )
        MongoDBUtils.remove_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_UID, identifier],
        )

        this_embed = RemoveEmbed.get_removed_key_embed(key_name=self.key_name)
        await interaction.response.edit_message(view=None, content=None, embed=this_embed)

        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.REMOVE_KEY,
            description=self.key_name,
        )
        await general.update_server_dashboard(guild=interaction.guild)

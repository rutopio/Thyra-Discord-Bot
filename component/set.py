import os
import discord
import traceback
from dotenv import load_dotenv

from component.welcome import WelcomeView

from embed.set import SetEmbed
from embed.bot import BotEmbed

from contents.view.set import SetViewContent

from constants.guild_operation import GUILD_OPERATION
from constants.db.guild_info import DB_GUILD_INFO

from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class SetDashboardChannelConfirmButton(discord.ui.Button):

    def __init__(self, ctx, channel_selector, this_embed):

        super().__init__(
            style=discord.ButtonStyle.success,
            label=SetViewContent.set_dashboard_channel_confirm_button_label,
            emoji=SetViewContent.set_dashboard_channel_confirm_button_emoji,
            row=1,
            disabled=True,
            custom_id=SetViewContent.set_dashboard_channel_confirm_button_id,
        )
        self.ctx = ctx
        self.channel_selector = channel_selector
        self.this_embed = this_embed

    async def callback(self, interaction: discord.Interaction):
        new_channel_id = int(self.channel_selector.selected_option)
        dashboard_channel = interaction.guild.get_channel(new_channel_id)
        if dashboard_channel:
            former_dashboard = MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
            )
            if former_dashboard:
                try:
                    announcement_message = await general.get_announcement_by_id(
                        guild=interaction.guild,
                        details=former_dashboard,
                    )
                    if announcement_message:
                        await announcement_message.delete()
                except:
                    print(traceback.format_exc())
                    # dialog does not exist, nothing to do
                    pass

            channel_mention = dashboard_channel.mention
            await interaction.response.edit_message(
                view=None,
                embed=SetEmbed.get_dashboard_channel_updated_embed(
                    channel_mention=channel_mention,
                    user_name=interaction.user.name,
                ),
            )

            tutorial_embed = BotEmbed.get_bot_tutorial_embed()
            log_embed = BotEmbed.get_bot_log_embed(guild=self.ctx.guild)
            status_embed = await BotEmbed.get_bot_dashboard_embed(guild=self.ctx.guild)

            announcement = await dashboard_channel.send(embeds=[tutorial_embed, log_embed, status_embed])
            announcement_id = announcement.id

            record = {
                DB_GUILD_INFO.DASHBOARD_CH__ID: new_channel_id,
                DB_GUILD_INFO.DASHBOARD_CH__ANNOUNCEMENT_ID: announcement_id,
            }
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                data_to_insert=record,
                sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
            )

            LogUtils.log_guild_activity(
                guild=interaction.guild,
                user=interaction.user,
                event=GUILD_OPERATION.SET_DASHBOARD_CH,
                description=[dashboard_channel, dashboard_channel.id],
            )

            await general.update_server_dashboard(guild=interaction.guild)


class SetVerificationChannelConfirmButton(discord.ui.Button):

    def __init__(self, ctx, channel_selector, this_embed):
        super().__init__(
            style=discord.ButtonStyle.success,
            label=SetViewContent.set_verification_channel_confirm_button_label,
            emoji=SetViewContent.set_verification_channel_confirm_button_emoji,
            row=1,
            disabled=True,
            custom_id=SetViewContent.set_verification_channel_confirm_button_id,
        )
        self.ctx = ctx
        self.channel_selector = channel_selector
        self.this_embed = this_embed

    async def callback(self, interaction: discord.Interaction):
        new_channel_id = int(self.channel_selector.selected_option)
        new_verification_channel = interaction.guild.get_channel(new_channel_id)

        if new_verification_channel:
            # remove the original dialog
            former_verification = MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                sub_keys=[DB_GUILD_INFO.VERIFICATION_CH],
            )
            if former_verification:
                try:
                    announcement_message = await general.get_announcement_by_id(
                        guild=interaction.guild,
                        details=former_verification,
                    )
                    if announcement_message:
                        await announcement_message.delete()
                except:
                    print(traceback.format_exc())
                    # dialog does not exist, nothing to do
                    pass
            channel_mention = new_verification_channel.mention
            await interaction.response.edit_message(
                view=None,
                embed=SetEmbed.get_verification_channel_updated_embed(
                    channel_mention=channel_mention,
                    user_name=interaction.user.name,
                ),
            )

            this_embed = SetEmbed.get_hi_there_embed()
            this_view = WelcomeView()

            announcement = await new_verification_channel.send(embed=this_embed, view=this_view)
            announcement_id = announcement.id

            record = {
                DB_GUILD_INFO.VERIFICATION_CH__ID: new_channel_id,
                DB_GUILD_INFO.VERIFICATION_CH__ANNOUNCEMENT_ID: announcement_id,
            }
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                data_to_insert=record,
                sub_keys=[DB_GUILD_INFO.VERIFICATION_CH],
            )

            LogUtils.log_guild_activity(
                guild=interaction.guild,
                user=interaction.user,
                event=GUILD_OPERATION.SET_VERIFICATION_CH,
                description=[new_verification_channel, new_verification_channel.id],
            )

            await general.update_server_dashboard(guild=interaction.guild)

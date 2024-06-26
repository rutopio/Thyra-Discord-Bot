import os
import discord
from dotenv import load_dotenv

from component.general import BasicViewComponent, ChannelSelector, CancelButton
from component.set import SetDashboardChannelConfirmButton, SetVerificationChannelConfirmButton
from embed.set import SetEmbed
from contents.view.set import SetViewContent

from constants.db.guild_info import DB_GUILD_INFO
from utils.mongodb import MongoDBUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class SetView():

    @staticmethod
    def add_embed_field_if_no_announcement(guild, this_embed):
        guild_id = guild.id
        this_embed.add_field(
            name=SetViewContent.channel_string,
            value=SetViewContent.channel_not_found_string,
            inline=False,
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            data_to_insert={},
            sub_keys=[DB_GUILD_INFO.VERIFICATION_CH],
        )

    @staticmethod
    async def get_verification_channel_embed_and_view(ctx):
        this_embed = SetEmbed.get_verification_channel_setting_embed()
        is_announcement_exist = False
        try:
            if MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.VERIFICATION_CH],
            ):
                current_dialog_channel_id = MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.VERIFICATION_CH, DB_GUILD_INFO.VERIFICATION_CH__ID],
                )
                current_dialog = MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.VERIFICATION_CH, DB_GUILD_INFO.VERIFICATION_CH__ANNOUNCEMENT_ID],
                )

                if ctx.guild.get_channel(current_dialog_channel_id):
                    msg = await ctx.guild.get_channel(current_dialog_channel_id).fetch_message(current_dialog)
                    if msg:
                        this_embed.add_field(
                            name=SetViewContent.channel_string,
                            value=ctx.guild.get_channel(current_dialog_channel_id).mention,
                            inline=False,
                        )
                        is_announcement_exist = True
        except:
            pass

        if not is_announcement_exist:
            SetView.add_embed_field_if_no_announcement(guild=ctx.guild, this_embed=this_embed)

        channel_selector = ChannelSelector(confirm_button=None)
        confirm_button = SetVerificationChannelConfirmButton(
            ctx=ctx,
            channel_selector=channel_selector,
            this_embed=this_embed,
        )
        channel_selector.confirm_button = confirm_button

        canceled_button = CancelButton(row=1)

        this_view = BasicViewComponent()
        this_view.add_item(channel_selector)
        this_view.add_item(confirm_button)
        this_view.add_item(canceled_button)

        return this_embed, this_view

    @staticmethod
    async def get_dashboard_channel_embed_and_view(ctx):
        this_embed = SetEmbed.get_dashboard_channel_setting_embed()
        is_announcement_exist = False
        try:
            if MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.DASHBOARD_CH],
            ):
                current_dialog_channel_id = MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.DASHBOARD_CH, DB_GUILD_INFO.DASHBOARD_CH__ID],
                )
                current_dialog = MongoDBUtils.query_by_keys(
                    db_name=DATABASE_NAME,
                    collection_name=GUILD_COLLECTION_NAME,
                    query_key=DB_GUILD_INFO.ID,
                    query_val=ctx.guild_id,
                    sub_keys=[DB_GUILD_INFO.DASHBOARD_CH, DB_GUILD_INFO.DASHBOARD_CH__ANNOUNCEMENT_ID],
                )

                if ctx.guild.get_channel(current_dialog_channel_id):
                    msg = await ctx.guild.get_channel(current_dialog_channel_id).fetch_message(current_dialog)
                    if msg:
                        this_embed.add_field(
                            name=SetViewContent.channel_string,
                            value=ctx.guild.get_channel(current_dialog_channel_id).mention,
                            inline=False,
                        )
                        is_announcement_exist = True
        except:
            pass

        if not is_announcement_exist:
            SetView.add_embed_field_if_no_announcement(guild=ctx.guild, this_embed=this_embed)

        channel_selector = ChannelSelector(confirm_button=None)
        confirm_button = SetDashboardChannelConfirmButton(
            ctx=ctx,
            channel_selector=channel_selector,
            this_embed=this_embed,
        )
        channel_selector.confirm_button = confirm_button

        canceled_button = CancelButton(row=1)

        this_view = BasicViewComponent()
        this_view.add_item(channel_selector)
        this_view.add_item(confirm_button)
        this_view.add_item(canceled_button)

        return this_embed, this_view

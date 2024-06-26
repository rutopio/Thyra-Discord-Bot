import discord
from discord.ext import commands

from content.commands.detail import DetailCommandContent

from embed.detail import DetailEmbed
from embed.general import GeneralEmbed

from view.detail import DetailView

from constant.db.key_info import DB_KEY_INFO
from constant.enum.key_type import KEY_TYPE
from utils.key import KeyUtils
from utils import general


class StatsCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    list_commands_group = discord.SlashCommandGroup(
        name=DetailCommandContent.detail_commands_group_name,
        description=DetailCommandContent.detail_commands_group_description,
    )

    @list_commands_group.command(
        name=DetailCommandContent.detail_key_command,
        description=DetailCommandContent.detail_key_description,
    )
    async def detail_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=DetailCommandContent.detail_key_name_option,
            description=DetailCommandContent.detail_key_name_option_description,
            autocomplete=general.key_name_autocomplete,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        key_info = KeyUtils.get_key_info_by_name(guild=ctx.guild, key_name=key_name)
        if key_info:
            this_embed = DetailEmbed.get_key_details_embed(ctx=ctx, key_info=key_info)
            if key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY:
                this_view = DetailView.get_otp_info_view(ctx=ctx, key_info=key_info)
                await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)
            else:
                await ctx.response.send_message(embed=this_embed, view=None, ephemeral=True)
        else:
            key_name_not_found_embed = GeneralEmbed.get_key_not_found_embed(key_name=key_name)
            await ctx.response.send_message(embed=key_name_not_found_embed, ephemeral=True)

    @list_commands_group.command(
        name=DetailCommandContent.detail_member_command,
        description=DetailCommandContent.detail_member_description,
    )
    async def detail_member(
        self,
        ctx: discord.ApplicationContext,
        member_id: discord.Option(
            str,
            name=DetailCommandContent.detail_member_name_option,
            description=DetailCommandContent.detail_member_name_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        if not member_id.isdigit():
            invalid_id_embed = DetailEmbed.get_invalid_user_id_embed(member_id=member_id)
            await ctx.response.send_message(embed=invalid_id_embed, ephemeral=True)
            return

        this_embed = DetailEmbed.get_user_details_embed(ctx=ctx, member_id=member_id)
        await ctx.response.send_message(embed=this_embed, ephemeral=True)

    @list_commands_group.command(
        name=DetailCommandContent.detail_pin_command,
        description=DetailCommandContent.detail_pin_description,
    )
    async def detail_pin(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=DetailCommandContent.detail_pin_key_name_option,
            description=DetailCommandContent.detail_pin_key_name_option_description,
            autocomplete=general.protected_keys_auto_complete,
        ),
        pin: discord.Option(
            str,
            name=DetailCommandContent.detail_pin_name_option,
            description=DetailCommandContent.detail_pin_name_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        key_info = KeyUtils.get_key_info_by_name(guild=ctx.guild, key_name=key_name)
        if key_info:
            if key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY:
                this_embed = DetailEmbed.get_pin_related_key_embed(ctx=ctx, key_info=key_info, pin_code=pin)
            else:
                this_embed = DetailEmbed.get_key_type_not_protected_embed(key_name=key_name)
        else:
            this_embed = GeneralEmbed.get_key_not_found_embed(key_name=key_name)

        await ctx.response.send_message(embed=this_embed, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(StatsCogs(bot))

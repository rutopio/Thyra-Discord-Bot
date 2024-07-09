import discord
from discord.ext import commands

from constant.guild_operation import GUILD_OPERATION
from content.commands.set import SetCommandContent
from embed.set import SetEmbed
from view.set import SetView
from utils.logs import LogUtils
from utils.times import TimeUtils
from utils import general


class SetCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    set_commands_group = discord.SlashCommandGroup(
        name=SetCommandContent.set_commands_group_name,
        description=SetCommandContent.set_commands_group_description,
    )

    @set_commands_group.command(
        name=SetCommandContent.set_verification_command,
        description=SetCommandContent.set_verification_description,
    )
    async def set_verification(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed, this_view = await SetView.get_verification_channel_embed_and_view(ctx=ctx)
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)

    @set_commands_group.command(
        name=SetCommandContent.set_dashboard_command,
        description=SetCommandContent.set_dashboard_description,
    )
    async def set_dashboard(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed, this_view = await SetView.get_dashboard_channel_embed_and_view(ctx=ctx)
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)

    @set_commands_group.command(
        name=SetCommandContent.set_timezone_command,
        description=SetCommandContent.set_timezone_description,
    )
    async def set_timezone(
        self,
        ctx: discord.ApplicationContext,
        timezone: discord.Option(
            str,
            name=SetCommandContent.set_timezone_tz_option,
            description=SetCommandContent.set_timezone_tz_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        if TimeUtils.is_timezone_valid(timezone_offset=timezone):
            this_embed = SetEmbed.get_valid_timezone_embed(guild=ctx.guild, timezone=timezone)
            await ctx.respond(embed=this_embed, ephemeral=True)
            LogUtils.log_guild_activity(
                guild=ctx.guild,
                user=ctx.user,
                event=GUILD_OPERATION.SET_TIMEZONE,
                description=str(timezone),
            )
        else:
            this_embed = SetEmbed.get_invalid_timezone_embed(value=timezone)
            await ctx.respond(embed=this_embed, ephemeral=True)
        await general.update_server_dashboard(guild=ctx.guild)


def setup(bot: discord.Bot):
    bot.add_cog(SetCogs(bot))

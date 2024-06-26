import discord
from discord.ext import commands

from content.commands.other import OtherCommandContent
from embed.bot import BotEmbed
from utils import general


class OtherCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(
        name=OtherCommandContent.tutorial_command,
        description=OtherCommandContent.tutorial_description,
    )
    async def tutorial(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        await ctx.respond(embed=BotEmbed.get_bot_tutorial_embed(), ephemeral=True)

    @commands.slash_command(
        name=OtherCommandContent.update_command,
        description=OtherCommandContent.update_description,
    )
    async def update_dashboard(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        await general.update_server_dashboard(guild=ctx.guild)
        await ctx.respond(embed=BotEmbed.get_dashboard_updated(), ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(OtherCogs(bot))

import discord
from discord.ext import commands

from constant.enum.key_type import KEY_TYPE
from content.commands.list import ListCommandContent
from embed.list import ListEmbed
from utils import general


class ListCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    list_commands_group = discord.SlashCommandGroup(
        name=ListCommandContent.list_commands_group_name,
        description=ListCommandContent.list_commands_group_description,
    )

    @list_commands_group.command(
        name=ListCommandContent.regular_key_command,
        description=ListCommandContent.regular_key_description,
    )
    async def list_regular(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed = ListEmbed.get_list_embed(ctx=ctx, list_key_type=KEY_TYPE.REGULAR_KEY)
        await ctx.response.send_message(embed=this_embed, ephemeral=True)
        # await general.update_server_dashboard(guild=ctx.guild)

    @list_commands_group.command(
        name=ListCommandContent.limited_key_command,
        description=ListCommandContent.limited_key_description,
    )
    async def list_limited(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed = ListEmbed.get_list_embed(ctx=ctx, list_key_type=KEY_TYPE.LIMITED_KEY)
        await ctx.response.send_message(embed=this_embed, ephemeral=True)
        # await general.update_server_dashboard(guild=ctx.guild)

    @list_commands_group.command(
        name=ListCommandContent.protected_key_command,
        description=ListCommandContent.protected_key_description,
    )
    async def list_one_time(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed = ListEmbed.get_list_embed(ctx=ctx, list_key_type=KEY_TYPE.PROTECTED_KEY)
        await ctx.response.send_message(embed=this_embed, ephemeral=True)
        # await general.update_server_dashboard(guild=ctx.guild)

    @list_commands_group.command(
        name=ListCommandContent.all_key_command,
        description=ListCommandContent.all_key_description,
    )
    async def list_all(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed = ListEmbed.get_list_embed(ctx=ctx, list_key_type=KEY_TYPE.ALL_KEYS)
        await ctx.response.send_message(embed=this_embed, ephemeral=True)
        # await general.update_server_dashboard(guild=ctx.guild)


def setup(bot: discord.Bot):
    bot.add_cog(ListCogs(bot))

import discord
from discord.ext import commands

from content.commands.remove import RemoveCommandContent
from embed.general import GeneralEmbed
from view.remove import RemoveView
from utils import general
from utils.key import KeyUtils


class RemoveCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    remove_commands_group = discord.SlashCommandGroup(
        name=RemoveCommandContent.remove_commands_group_name,
        description=RemoveCommandContent.remove_commands_group_description,
    )

    @remove_commands_group.command(
        name=RemoveCommandContent.remove_key_command,
        description=RemoveCommandContent.remove_key_description,
    )
    async def remove_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=RemoveCommandContent.remove_key_name_option,
            description=RemoveCommandContent.remove_key_name_option_description,
            autocomplete=general.key_name_autocomplete,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        key_info = KeyUtils.get_key_info_by_name(guild=ctx.guild, key_name=key_name)
        if key_info:
            this_embed, this_view = RemoveView.get_removing_key_embed_and_view(ctx=ctx, key_info=key_info)
            await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)
            return
        else:
            key_name_not_found_embed = GeneralEmbed.get_key_not_found_embed(key_name=key_name)
            await ctx.response.send_message(embed=key_name_not_found_embed, ephemeral=True)

    @remove_commands_group.command(
        name=RemoveCommandContent.remove_all_command,
        description=RemoveCommandContent.remove_all_description,
    )
    async def remove_all(self, ctx: discord.ApplicationContext):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return
        this_embed, this_view = RemoveView.get_removing_all_embed_and_view(ctx=ctx)
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(RemoveCogs(bot))

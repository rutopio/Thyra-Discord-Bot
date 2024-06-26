import discord
from discord.ext import commands

from contents.commands.edit import EditCommandContent
from embed.general import GeneralEmbed
from utils import general
from utils.key import KeyUtils


class EditCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    remove_commands_group = discord.SlashCommandGroup(
        name=EditCommandContent.edit_commands_group_name,
        description=EditCommandContent.edit_commands_group_description,
    )

    @remove_commands_group.command(
        name=EditCommandContent.edit_key_command,
        description=EditCommandContent.edit_key_description,
    )
    async def edit_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=EditCommandContent.edit_key_name_option,
            description=EditCommandContent.edit_key_name_option_description,
            autocomplete=general.key_name_autocomplete,
        ),
    ):

        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        key_info = KeyUtils.get_key_info_by_name(guild=ctx.guild, key_name=key_name)
        if key_info:
            from view.edit import EditView
            this_embed, this_view = EditView.get_editing_embed_and_view(ctx=ctx, key_info=key_info)
            await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)
        else:
            key_name_not_found_embed = GeneralEmbed.get_key_not_found_embed(key_name=key_name)
            await ctx.response.send_message(embed=key_name_not_found_embed, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(EditCogs(bot))

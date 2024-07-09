import discord
from discord.ext import commands

from constant.enum.key_type import KEY_TYPE
from content.commands.create import CreateCommandContent
from view.create import CreateView
from utils.key import KeyUtils
from utils import general


class CreateCogs(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    create_commands_group = discord.SlashCommandGroup(
        name=CreateCommandContent.create_commands_group_name,
        description=CreateCommandContent.create_commands_group_description,
    )

    @create_commands_group.command(
        name=CreateCommandContent.regular_key_command,
        description=CreateCommandContent.regular_key_description,
    )
    async def create_regular_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=CreateCommandContent.regular_key_name_option,
            description=CreateCommandContent.regular_key_name_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        if await KeyUtils.callback_if_key_out_of_quota(ctx=ctx, key_type=KEY_TYPE.REGULAR_KEY):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_too_long(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_exists(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return

        this_embed, this_view = CreateView.get_creating_embed_and_view(
            ctx=ctx,
            key_name=general.encode_text(string=key_name),
            key_type=KEY_TYPE.REGULAR_KEY,
        )
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)

    @create_commands_group.command(
        name=CreateCommandContent.limited_key_command,
        description=CreateCommandContent.limited_key_description,
    )
    async def create_limited_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=CreateCommandContent.limited_key_name_option,
            description=CreateCommandContent.limited_key_name_option_description,
        ),
        times: discord.Option(
            int,
            name=CreateCommandContent.limited_key_times_option,
            min_value=1,
            description=CreateCommandContent.limited_key_times_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        if await KeyUtils.callback_if_key_out_of_quota(ctx=ctx, key_type=KEY_TYPE.LIMITED_KEY):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_too_long(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_exists(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return

        if await KeyUtils.callback_usage_limit_number_invalid(ctx=ctx, number=times):
            await general.update_server_dashboard(guild=ctx.guild)
            return

        this_embed, this_view = CreateView.get_creating_embed_and_view(
            ctx=ctx,
            key_name=general.encode_text(string=key_name),
            key_type=KEY_TYPE.LIMITED_KEY,
            times=times,
        )
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)

    @create_commands_group.command(
        name=CreateCommandContent.protected_key_command,
        description=CreateCommandContent.protected_key_description,
    )
    async def create_protected_key(
        self,
        ctx: discord.ApplicationContext,
        key_name: discord.Option(
            str,
            name=CreateCommandContent.protected_key_name_option,
            description=CreateCommandContent.protected_key_name_option_description,
        ),
        number: discord.Option(
            int,
            name=CreateCommandContent.protected_key_number_option,
            min_value=1,
            description=CreateCommandContent.protected_key_number_option_description,
        ),
    ):
        if not await general.is_admin_reply(bot=self.bot, ctx=ctx):
            return

        if await KeyUtils.callback_if_key_out_of_quota(ctx=ctx, key_type=KEY_TYPE.PROTECTED_KEY):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_too_long(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return
        if await KeyUtils.callback_if_key_name_exists(ctx=ctx, key_name=key_name):
            await general.update_server_dashboard(guild=ctx.guild)
            return

        if await KeyUtils.callback_if_otp_number_invalid(ctx=ctx, num_otp=number):
            await general.update_server_dashboard(guild=ctx.guild)
            return

        this_embed, this_view = CreateView.get_creating_embed_and_view(
            ctx=ctx,
            key_name=general.encode_text(string=key_name),
            key_type=KEY_TYPE.PROTECTED_KEY,
            times=number,
        )
        await ctx.response.send_message(embed=this_embed, view=this_view, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(CreateCogs(bot))

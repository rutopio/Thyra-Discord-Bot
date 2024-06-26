import discord
from utils.times import TimeUtils


class GeneralContent():

    discord_presence = 'Thyra Bot @ Github/rutopio'
    divider = '-' * 50

    def mongodb_connected_successfully():
        return f"{TimeUtils.get_utc_now()} |  You've successfully connected to MongoDB..."

    def mongodb_connected_failed():
        return f'{TimeUtils.get_utc_now()} |  MongoDB Server is not available...'

    def module_loaded(cog_name):
        return f'{TimeUtils.get_utc_now()} |  Module Loaded: {cog_name}'

    def bot_logged_in(bot: discord.Bot):
        return f'{TimeUtils.get_utc_now()} |  {bot.user} is online...'

    def bot_logging(bot: discord.Bot):
        return f'{TimeUtils.get_utc_now()} |  Now Logging...'

    def dashboard_updated(bot: discord.Bot):
        return f'{TimeUtils.get_utc_now()} |  All dashboard in servers have been updated to the latest...'

    def dashboard_init_guild(idx, bot: discord.Bot, guild):
        return f'{TimeUtils.get_utc_now()} |  [{idx}/{len(bot.guilds)}] (init) {guild}...'

    def dashboard_sync_guild(idx, bot: discord.Bot, guild):
        return f'{TimeUtils.get_utc_now()} |  [{idx}/{len(bot.guilds)}] (sync) {guild}...'

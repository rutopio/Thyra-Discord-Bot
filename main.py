import os
import discord
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv

from component.welcome import WelcomeView
from constant.db.guild_info import DB_GUILD_INFO
from constant.db.log_info import DB_LOG_INFO
from content.general import GeneralContent

from utils import general
from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')
DATABASE_URI = os.getenv('MONGODB_URL')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    bot.add_view(WelcomeView())
    game = discord.Game(GeneralContent.discord_presence)
    await bot.change_presence(status=discord.Status.idle, activity=game)

    print(GeneralContent.bot_logged_in(bot))

    for idx, guild in enumerate(bot.guilds):
        if not MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=guild.id,
        ):
            await general.initialize_for_guild(guild)
            print(GeneralContent.dashboard_init_guild(idx=idx + 1, bot=bot, guild=guild))
        else:
            await general.update_server_dashboard(guild)
            print(GeneralContent.dashboard_sync_guild(idx=idx + 1, bot=bot, guild=guild))

    print(GeneralContent.dashboard_updated(bot))
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_READY},
    )
    print(GeneralContent.bot_logging(bot))


@bot.event
async def on_disconnect():
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_DISCONNECT},
    )


@bot.event
async def on_error(event, *args, **kwargs):
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_ERROR},
    )


@bot.event
async def on_resumed():
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_RESUMED},
    )


@bot.event
async def on_guild_join(guild: discord.Guild):
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={
            DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_GUILD_JOIN,
            DB_LOG_INFO.STATUS__GUILD_NAME: guild.name,
            DB_LOG_INFO.STATUS__GUILD_ID: guild.id
        },
    )
    await general.initialize_for_guild(guild)
    print(GeneralContent.guild_joined(guild=guild))


@bot.event
async def on_guild_remove(guild: discord.Guild):
    LogUtils.log_to_json(
        log_type=DB_LOG_INFO.STATUS,
        record={
            DB_LOG_INFO.STATUS__EVENT: DB_LOG_INFO.ON_GUILD_REMOVE,
            DB_LOG_INFO.STATUS__GUILD_NAME: guild.name,
            DB_LOG_INFO.STATUS__GUILD_ID: guild.id
        },
    )
    MongoDBUtils.move_document_to_abandon_collection(
        db_name=DATABASE_NAME,
        query_key=DB_GUILD_INFO.ID,
        query_val=guild.id,
        from_collection_name=GUILD_COLLECTION_NAME,
    )
    print(GeneralContent.guild_left(guild=guild))


@bot.event
async def on_guild_update(before_guild: discord.Guild, after_guild: discord.Guild):
    MongoDBUtils.update_by_keys(
        db_name=DATABASE_NAME,
        collection_name=GUILD_COLLECTION_NAME,
        query_key=DB_GUILD_INFO.ID,
        query_val=before_guild.id,
        data_to_insert=after_guild.name,
        sub_keys=[DB_GUILD_INFO.NAME],
    )


if __name__ == '__main__':
    # Create a new client and connect to the server
    client = MongoDBUtils.get_mongodb_client(DATABASE_URI)

    try:
        # Send a ping to confirm a successful connection
        print(client.admin.command('ping'))
        print(GeneralContent.mongodb_connected_successfully())
    except Exception as e:
        print(e)
        print(GeneralContent.mongodb_connected_failed())
        return

    print(GeneralContent.divider)

    for cog in [p.stem for p in Path('.').glob('./cog/*.py')]:
        bot.load_extension(f'cog.{cog}')
        print(GeneralContent.module_loaded(cog_name=cog))
    print(GeneralContent.divider)

bot.run(DISCORD_TOKEN)

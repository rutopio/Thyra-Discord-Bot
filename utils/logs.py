import os
import traceback
import datetime
from dotenv import load_dotenv
import json

from embed.bot import BotEmbed

from constant.usage_limits import USAGE_LIMIT
from constant.guild_operation import GUILD_OPERATION
from constant.db.guild_info import DB_GUILD_INFO
from constant.db.key_info import DB_KEY_INFO
from constant.db.log_info import DB_LOG_INFO

from utils.times import TimeUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class LogUtils():

    @staticmethod
    def log_to_json(log_type, record):
        current_timestamp, formatted_time = TimeUtils.get_utc_now_timestamp()
        current_timestamp = str(current_timestamp)
        time_dict = {DB_LOG_INFO.TIME: formatted_time}
        file_path = f'{DB_LOG_INFO.LOG_FOLDER_PATH}/{log_type}.{DB_LOG_INFO.LOG_FILE_FORMAT}'
        try:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write('{}')

            with open(file_path, 'r') as file:
                data = json.load(file)
            data[current_timestamp] = {**time_dict, **record}
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except:
            print(traceback.format_exc())

    @staticmethod
    def log_guild_activity(guild, user, event, description):
        user_id = user.id

        guild_id = guild.id
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        edit_identifier = KeyUtils.get_key_identifier_by_timestamp(current_timestamp)

        if event in [GUILD_OPERATION.SET_DASHBOARD_CH, GUILD_OPERATION.SET_VERIFICATION_CH]:
            channel_mention = description[0].mention
            channel_id = description[1]
            record = {
                DB_GUILD_INFO.LOGS__USER_ID: user_id,
                DB_GUILD_INFO.LOGS__LOGGED_AT: current_timestamp,
                DB_GUILD_INFO.LOGS__EVENT: event,
                DB_GUILD_INFO.LOGS__DETAILS: channel_mention,
            }
            description = f'{channel_id}'

        else:
            record = {
                DB_GUILD_INFO.LOGS__USER_ID: user_id,
                DB_GUILD_INFO.LOGS__LOGGED_AT: current_timestamp,
                DB_GUILD_INFO.LOGS__EVENT: event,
                DB_GUILD_INFO.LOGS__DETAILS: description,
            }

            if type(description) is list:
                description = [general.escape_html(i) for i in description]
            else:
                description = general.escape_html(description)

        LogUtils.log_to_json(
            log_type=DB_LOG_INFO.ACTIVITY,
            record={
                DB_LOG_INFO.ACTIVITY__EVENT: event,
                DB_LOG_INFO.ACTIVITY__DETAILS: description,
                DB_LOG_INFO.ACTIVITY__GUILD_NAME: guild.name,
                DB_LOG_INFO.ACTIVITY__GUILD_ID: guild.id,
                DB_LOG_INFO.ACTIVITY__USER_NAME: user.name,
                DB_LOG_INFO.ACTIVITY__USER_ID: user.id
            },
        )

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            data_to_insert=record,
            sub_keys=[DB_GUILD_INFO.LOGS, edit_identifier],
        )

        logs = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.LOGS],
        )

        while len(logs) > USAGE_LIMIT.MAX_NUMBER_OF_GUILD_LOGS():
            oldest_timestamp = min(logs.keys())
            del logs[oldest_timestamp]

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            data_to_insert=logs,
            sub_keys=[DB_GUILD_INFO.LOGS],
        )

    @staticmethod
    def log_key_edited_history(interaction, identifier, event, old_value):
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        edit_identifier = KeyUtils.get_key_identifier_by_timestamp(current_timestamp)

        record = {
            DB_KEY_INFO.EDITED__USER_ID: interaction.user.id,
            DB_KEY_INFO.EDITED__AT: current_timestamp,
            DB_KEY_INFO.EDITED__EVENT: event,
            DB_KEY_INFO.EDITED__PREVIOUS_VALUE: old_value,
        }

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=record,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.EDITED, edit_identifier],
        )

        logs = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.EDITED],
        )
        while len(logs) > USAGE_LIMIT.MAX_NUMBER_OF_EDITED_KEY_LOGS():
            oldest_timestamp = min(logs.keys())
            del logs[oldest_timestamp]

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=logs,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.EDITED],
        )

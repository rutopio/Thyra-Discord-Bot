import os
import re
import datetime
from dotenv import load_dotenv

from content.utils.time import TimeUtilsContent

from constant.db.guild_info import DB_GUILD_INFO
from constant.constants import CONSTANT

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class TimeUtils():

    def get_utc_now():
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc)
        utc_now = current_timestamp + datetime.timedelta(hours=0)
        formatted_time = utc_now.strftime(CONSTANT.DATE_FORMAT)
        return formatted_time

    def get_utc_now_timestamp():
        current_timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        current_time = datetime.datetime.now(tz=datetime.timezone.utc)
        utc_now = current_time + datetime.timedelta(hours=0)
        formatted_time = utc_now.strftime(CONSTANT.DATE_FORMAT)
        return int(current_timestamp), str(formatted_time)

    def is_timezone_valid(timezone_offset):
        pattern = r'^[-+](0[0-9]|1[0-2])(00|15|30|45)$'

        if re.match(pattern, timezone_offset):
            return True
        else:
            return False

    def convert_to_local_timestamp(guild, utc_timestamp):
        from utils.mongodb import MongoDBUtils
        guild_id = guild.id
        utc_datetime = datetime.datetime.utcfromtimestamp(utc_timestamp)

        timezone_offset = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=guild_id,
            sub_keys=[DB_GUILD_INFO.TIMEZONE],
        )
        hours = int(timezone_offset[1:3])
        minutes = int(timezone_offset[3:])
        total_offset_minutes = (hours * 60 + minutes) * (-1 if timezone_offset[0] == '-' else 1)
        timezone_delta = datetime.timedelta(minutes=total_offset_minutes)
        datetime_in_timezone = utc_datetime + timezone_delta
        return datetime_in_timezone

    def get_timedelta_between_joined_and_use_key(joined_time, used_time):
        delta = used_time - joined_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        res = ''
        if days:
            res += f'{days}{TimeUtilsContent.day_string} '
        if hours:
            res += f'{hours}{TimeUtilsContent.hour_string} '
        if minutes:
            res += f'{minutes}{TimeUtilsContent.minute_string} '
        if seconds:
            res += f'{seconds}{TimeUtilsContent.second_string}'
        return res

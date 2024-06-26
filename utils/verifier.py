import os
import datetime
from dotenv import load_dotenv

from embed.set import SetEmbed

from constants.enum.key_type import KEY_TYPE
from constants.db.key_info import DB_KEY_INFO
from constants.db.guild_info import DB_GUILD_INFO
from constants.db.user_info import DB_USER_INFO
from constants.role_selector import ROLE_SELECTOR

from utils.role import RoleUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')
USER_COLLECTION_NAME = os.getenv('USER_COLLECTION_NAME')


class Verifier():

    def __init__(self, interaction, guild, user, key_name, pin=''):
        self.interaction = interaction
        self.guild = guild
        self.guild_id = guild.id
        self.key_name = key_name
        self.identifier = None
        self.pin = pin
        self.user = user
        self.key_info = None
        self.key_type = None
        self.is_verified = False

    async def get_auth_embed(self):
        embed = await self.steps_by_steps()
        # print('self.is_verified', self.is_verified)
        return self.is_verified, embed

    async def steps_by_steps(self):
        if not self.is_key_valid_and_activate():
            # print('is_key_valid_and_activate')
            return SetEmbed.get_invalid_key_or_pin_embed(self.interaction.user)

        self.key_type = self.key_info[DB_KEY_INFO.TYPE]

        if self.is_user_used_key_before():
            # print('is_user_used_key_before')
            return SetEmbed.get_user_used_key_before_embed()

        if self.key_type == KEY_TYPE.REGULAR_KEY:
            return await self.verify_regular_key()
        elif self.key_type == KEY_TYPE.LIMITED_KEY:
            return await self.verify_limited_key()
        elif self.key_type == KEY_TYPE.PROTECTED_KEY:
            return await self.verify_one_time_pin()

    def is_key_valid_and_activate(self):
        name_id_relationship = KeyUtils.get_name_and_identifier_dict(self.guild)
        if self.key_name in name_id_relationship:
            self.identifier = name_id_relationship[self.key_name]
            self.key_info = KeyUtils.get_key_info_by_identifier(self.guild, self.identifier)
            if self.key_info[DB_KEY_INFO.STATUS]:
                return True
        return False

    def is_user_used_key_before(self):
        user_used_keys = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=USER_COLLECTION_NAME,
            query_key=DB_USER_INFO.USER_ID,
            query_val=self.user.id,
            sub_keys=[DB_USER_INFO.USED_KEYS, str(self.guild_id)],
        )

        if self.identifier in user_used_keys:
            return True
        else:
            return False

    async def verify_regular_key(self):
        if self.pin:
            return SetEmbed.get_invalid_key_or_pin_embed(user=self.interaction.user)
        else:
            return await self.insert_new_key_to_collections()

    async def verify_limited_key(self):
        if self.pin:
            return SetEmbed.get_invalid_key_or_pin_embed(user=self.interaction.user)

        if len(self.key_info[DB_KEY_INFO.USED_MEMBERS]) < int(self.key_info[DB_KEY_INFO.COUNT]):
            return await self.insert_new_key_to_collections()
        else:
            return SetEmbed.get_invalid_key_or_pin_embed(user=self.user)

    async def verify_one_time_pin(self):
        unused_pins = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=self.interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__UNUSED],
        )
        used_pins = list(
            MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=self.interaction.guild_id,
                sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__USED],
            ).keys())

        if self.pin in unused_pins and self.pin not in used_pins:
            self.drop_pin_from_unused_and_append_to_used(unused_pins=unused_pins, used_pins=used_pins)
            embed = await self.insert_new_key_to_collections()
            return embed
        else:
            # print('self.pin in unused_pins and self.pin not in used_pins')
            return SetEmbed.get_invalid_key_or_pin_embed(user=self.user)

    async def insert_new_key_to_collections(self):
        self.insert_used_user_to_guild_collection()
        self.insert_used_key_to_user_collection()
        added_roles_mentions = await RoleUtils.get_roles_mention_list_and_operate(
            interaction=self.interaction,
            role_list=self.key_info[DB_KEY_INFO.ASSIGN_ROLES],
            user=self.user,
            event=ROLE_SELECTOR.ASSIGN,
        )
        remove_roles_mentions = await RoleUtils.get_roles_mention_list_and_operate(
            interaction=self.interaction,
            role_list=self.key_info[DB_KEY_INFO.REMOVE_ROLES],
            user=self.user,
            event=ROLE_SELECTOR.REMOVE,
        )
        self.is_verified = True
        return SetEmbed.get_welcome_embed_after_verify(
            guild=self.guild,
            user=self.user,
            key_name=self.key_name,
            added_roles_mentions=added_roles_mentions,
            remove_roles_mentions=remove_roles_mentions,
        )

    def insert_used_user_to_guild_collection(self):
        current_ordinal = len(
            MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=self.guild_id,
                sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.USED_MEMBERS],
            ))
        if self.key_type == KEY_TYPE.PROTECTED_KEY:
            record = {
                DB_KEY_INFO.USED_MEMBERS__USER_ID: self.user.id,
                DB_KEY_INFO.USED_MEMBERS__TIMESTAMP: datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
                DB_KEY_INFO.USED_MEMBERS__ORDER: current_ordinal + 1,
                DB_KEY_INFO.USED_MEMBERS__PIN: self.pin,
            }
        else:
            record = {
                DB_KEY_INFO.USED_MEMBERS__USER_ID: self.user.id,
                DB_KEY_INFO.USED_MEMBERS__TIMESTAMP: datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
                DB_KEY_INFO.USED_MEMBERS__ORDER: current_ordinal + 1
            }

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=self.guild_id,
            data_to_insert=record,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.USED_MEMBERS,
                      str(self.user.id)],
        )

    def insert_used_key_to_user_collection(self):
        user_details = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=USER_COLLECTION_NAME,
            query_key=DB_USER_INFO.USER_ID,
            query_val=self.user.id,
        )

        if user_details:
            this_guild_keys_identifier = MongoDBUtils.query_by_keys(
                db_name=DATABASE_NAME,
                collection_name=USER_COLLECTION_NAME,
                query_key=DB_USER_INFO.USER_ID,
                query_val=self.user.id,
                sub_keys=[DB_USER_INFO.USED_KEYS, str(self.guild_id)],
            )

            if this_guild_keys_identifier:
                this_guild_keys_identifier.append(self.identifier)
            else:
                this_guild_keys_identifier = [self.identifier]

            record = {str(self.guild_id): this_guild_keys_identifier}
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=USER_COLLECTION_NAME,
                query_key=DB_USER_INFO.USER_ID,
                query_val=self.user.id,
                data_to_insert=record,
                sub_keys=[DB_USER_INFO.USED_KEYS],
            )
        else:
            record = {
                DB_USER_INFO.USER_ID: self.user.id,
                DB_USER_INFO.USED_KEYS: {
                    str(self.guild_id): [self.identifier],
                },
            }
            MongoDBUtils.get_collection(db_name=DATABASE_NAME, collection_name=USER_COLLECTION_NAME).insert_one(record)

    def drop_pin_from_unused_and_append_to_used(self, unused_pins, used_pins):
        unused_pins.remove(self.pin)
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=self.interaction.guild_id,
            data_to_insert=unused_pins,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__UNUSED],
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=self.interaction.guild_id,
            data_to_insert=self.user.id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, self.identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__USED, self.pin],
        )

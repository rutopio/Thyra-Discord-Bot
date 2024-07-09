import os
import datetime
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from constant.db.left_info import DB_LEFT_INFO
from utils import general

load_dotenv()
DATABASE_URI = os.getenv('MONGODB_URL')


class MongoDBUtils():

    @staticmethod
    def get_mongodb_client(database_uri):
        client = MongoClient(database_uri, server_api=ServerApi('1'))
        return client

    @staticmethod
    def get_collection(db_name, collection_name):
        client = MongoDBUtils.get_mongodb_client(DATABASE_URI)
        database = client[db_name]
        collection = database[collection_name]
        return collection

    @staticmethod
    def update_to_database(db_name, collection_name, data_to_insert, query_key):
        collection = MongoDBUtils.get_collection(db_name, collection_name)
        existing_document = collection.find_one(query_key)

        if existing_document:
            collection.replace_one(query_key, data_to_insert)
        else:
            collection.insert_one(data_to_insert)

    @staticmethod
    def remove_from_database(db_name, collection_name, query_key):
        collection = MongoDBUtils.get_collection(db_name, collection_name)
        result = collection.delete_one(query_key)

    @staticmethod
    def query_by_keys(db_name, collection_name, query_key, query_val, sub_keys=[]):
        query_key = str(query_key)
        collection = MongoDBUtils.get_collection(db_name, collection_name)
        existing_document = collection.find_one({query_key: query_val})
        keys = [str(i) for i in sub_keys]

        try:
            if existing_document:
                for key in keys:
                    existing_document = existing_document[key]
                return existing_document
            else:
                return {}
        except:
            return {}

    @staticmethod
    def update_by_keys(db_name, collection_name, query_key, query_val, data_to_insert, sub_keys=[]):
        query_key = str(query_key)
        collection = MongoDBUtils.get_collection(db_name, collection_name)
        existing_document = collection.find_one({query_key: query_val})
        keys = [general.escape_text(str(i)) for i in sub_keys]

        if existing_document:
            update_query = {'$set': {f'{".".join(keys)}': data_to_insert}}
            collection.update_one({query_key: query_val}, update_query, upsert=True)

    @staticmethod
    def remove_by_keys(db_name, collection_name, query_key, query_val, sub_keys=[]):
        query_key = str(query_key)

        collection = MongoDBUtils.get_collection(db_name, collection_name)
        existing_document = collection.find_one({query_key: query_val})
        keys = [general.escape_text(str(i)) for i in sub_keys]

        if existing_document:
            update_query = {'$unset': {f'{".".join(keys)}': 1}}
            collection.update_one({query_key: query_val}, update_query, upsert=True)

    @staticmethod
    def move_document_to_abandon_collection(
        db_name,
        query_key,
        query_val,
        from_collection_name,
        to_collection_name=None,
    ):
        if not to_collection_name:
            to_collection_name = f'{from_collection_name}{DB_LEFT_INFO.LEFT_SUFFIX}'

        collection = MongoDBUtils.get_collection(db_name, from_collection_name)
        existing_document = collection.find_one({query_key: query_val})
        if existing_document:
            existing_document[DB_LEFT_INFO.LEFT_AT] = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
            del existing_document['_id']

            abandon_database_name = DB_LEFT_INFO.LEFT_DATABASE_NAME
            abandon_collection = MongoDBUtils.get_collection(abandon_database_name, to_collection_name)
            abandon_collection.insert_one(existing_document)

            # delete from db
            collection.delete_one({query_key: query_val})

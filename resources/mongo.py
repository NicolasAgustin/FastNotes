"""Mongo connector"""

from decouple import config
from pymongo.mongo_client import MongoClient


class Mongo:
    """Mongo class"""

    def __init__(self):
        self.client = MongoClient(config("DB_HOST"), int(config("DB_PORT")))
        self.database = self.client.get_database(config("DB_NAME"))

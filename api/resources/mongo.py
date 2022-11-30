"""Mongo connector"""

import os

from pymongo.mongo_client import MongoClient


class Mongo:
    """Mongo class"""

    def __init__(self):
        self.client = MongoClient(os.getenv("DB_HOST"), int(os.getenv("DB_PORT")))
        self.database = self.client.get_database(os.getenv("DB_NAME"))

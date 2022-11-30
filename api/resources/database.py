"""Database module"""

from typing import List

from resources.mongo import Mongo


class Database:
    """Database connector"""

    def __init__(self):
        self.__client = Mongo()

    def find(self, collection: str, query: dict = None) -> List[dict]:
        """_summary_

        Args:
            collection (str): _description_
            query (dict, optional): _description_. Defaults to None.

        Returns:
            List[dict]: _description_
        """

        results = []

        if query is None:
            results = self.__client.database.get_collection(collection).find({})
        else:
            results = self.__client.database.get_collection(collection).find(query)

        return list(results)

    def find_one(self, collection: str, query: dict) -> dict:
        """_summary_

        Args:
            collection (str): _description_
            query (dict): _description_

        Returns:
            dict: _description_
        """
        return self.__client.database.get_collection(collection).find_one(query)

    def insert(self, collection: str, document: dict):
        """_summary_

        Args:
            collection (str): _description_
            document (dict): _description_
        """
        self.__client.database.get_collection(collection).insert_one(document)

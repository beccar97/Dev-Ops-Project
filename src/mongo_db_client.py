import pymongo
import datetime
from bson.objectid import ObjectId

from src.models.todo_item import Item
from src.mongo_config import MongoConfig
from src.mongo_collections import MongoCollection


class MongoClient:
    TODO_COLLECTION = MongoCollection('to_do', 'To Do')
    DOING_COLLECTION = MongoCollection('doing', 'Doing')
    DONE_COLLECTION = MongoCollection('done', 'Done')

    def __init__(self, mongo_config: MongoConfig):
        self.mongo_config = mongo_config
        connection_string = f"mongodb+srv://{mongo_config.user_name}:{mongo_config.password}@{mongo_config.mongo_url}/{mongo_config.default_database}?w=majority"
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[mongo_config.default_database]

    def create_database(self, name='todo_app', use_as_default=False):
        """
        Create a new mongo db with the given name.

        Args:
            name(str): The name of the database.
            use_as_default(boolean): Boolean indicating whether this database should be used 
            by default by this client
        """

        db = self.client[name]

        if use_as_default:
            self.db = db

        return db

    def delete_database(self, name):
        """
        Deletes the Atlas database with the given name.
        If the given database was the default database for this client, will create a new 
        database with the name determined by MongoConfig to use as default in future.

        Args:
            name (str): The id of the board to be deleted.
        """
        if (self.db.name == name):
            self.client.drop_database(name)
            self.db = self.client[self.mongo_config.default_database]
        else:
            self.client.drop_database(name)

        return

    def get_items(self):
        """
        Fetches all todo items from Atlas database.

        Returns:
            list: A list of the saved items
        """
        todo_items = self.db[self.TODO_COLLECTION.name].find()
        doing_items = self.db[self.DOING_COLLECTION.name].find()
        done_items = self.db[self.DONE_COLLECTION.name].find()

        all_items = []
        all_items.extend(todo_items)
        all_items.extend(doing_items)
        all_items.extend(done_items)

        items = list(map(self._as_app_item, all_items))

        return items

    def add_item(self, name):
        """
        Adds a new document with the specified name to the collection of not started tasks.

        Args:
            name (str): The name of the item.
        """

        todo_collection = self.db[self.TODO_COLLECTION.name]

        item_json = {
            "name": name,
            "status": 'To Do',
            "dateLastActivity": datetime.datetime.utcnow()
        }

        todo_collection.insert_one(item_json)

    def start_item(self, id):
        """
        Moves the item with the specified ID from the "To Do" collection to the "Doing" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.TODO_COLLECTION, self.DOING_COLLECTION)

    def complete_item(self, id):
        """
        Moves the item with the specified ID from the "Doing" collection to the "Done" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.DOING_COLLECTION, self.DONE_COLLECTION)

    def uncomplete_item(self, id):
        """
        Moves the item with the specified ID from the "Done" collection to the "Doing" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.DONE_COLLECTION, self.DOING_COLLECTION)

    def delete_item(self, id):
        """
        Deletes the item with the specified ID

        Args:
            id (str): The ID of the item.
        """
        id = ObjectId(id)
        collections = self.db.list_collection_names()

        for collection in collections:
            self.db[collection].delete_one({"_id": id})

    def _move_item(self, id, from_collection: MongoCollection, to_collection: MongoCollection):
        id = ObjectId(id)

        from_db_collection = self.db[from_collection.name]
        to_db_collection = self.db[to_collection.name]

        item = from_db_collection.find_one({"_id": id})
        item['status'] = to_collection.status

        to_db_collection.insert_one(item)
        from_db_collection.delete_one({"_id": id})

    def _as_app_item(self, item):
        return Item.from_mongo_document(item)

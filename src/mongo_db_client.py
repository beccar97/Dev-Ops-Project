import pymongo
import datetime
from bson.objectid import ObjectId
from flask import session, current_app as app
from flask_login import current_user as current_user

from src.models.todo_item import Item
from src.models.user import User, UserRole
from src.mongo_config import MongoConfig
from src.mongo_collections import MongoCollection


class MongoClient:
    TODO_COLLECTION = MongoCollection('to_do', 'To Do')
    DOING_COLLECTION = MongoCollection('doing', 'Doing')
    DONE_COLLECTION = MongoCollection('done', 'Done')

    def __init__(self, mongo_config: MongoConfig):
        self.mongo_config = mongo_config
        self.client = pymongo.MongoClient(mongo_config.connection_string)
        if hasattr(mongo_config, 'default_database') and mongo_config.default_database is not None:
            self.db = self.client[mongo_config.default_database]
        else:
            self.db = self.client.get_default_database()

    def create_database(self, name='todo_app', use_as_default=False):
        """
        Create a new mongo db with the given name.

        Args:
            name(str): The name of the database.
            use_as_default(boolean): Boolean indicating whether this database should be used
            by default by this client
        """

        db = self.client[name]
        app.logger.debug(f"Creating database {name}")
        if use_as_default:
            app.logger.debug(f"Setting {name} as default database")
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
        app.logger.debug(f"Dropping database {name}")
        if (self.db.name == name):
            self.client.drop_database(name)
            app.logger.warn(
                f"Database {name} is default database, recreating after dropping")
            self.db = self.client[self.mongo_config.default_database]
        else:
            app.logger.debug(f"Database {name} successfully dropped")
            self.client.drop_database(name)

        return

    # region items methods

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

    def add_item(self, name: str):
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

        added_item = todo_collection.insert_one(item_json)

        app.logger.debug(
            f"Item '{name}' added with id: {added_item.inserted_id}")

    def start_item(self, id: str):
        """
        Moves the item with the specified ID from the "To Do" collection to the "Doing" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.TODO_COLLECTION, self.DOING_COLLECTION)

        app.logger.debug(f"Item with id {id} started")

    def complete_item(self, id: str):
        """
        Moves the item with the specified ID from the "Doing" collection to the "Done" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.DOING_COLLECTION, self.DONE_COLLECTION)

        app.logger.debug(f"Item with id {id} marked as complete")

    def uncomplete_item(self, id: str):
        """
        Moves the item with the specified ID from the "Done" collection to the "Doing" collection in the database.

        Args:
            id (str): The ID of the item.
        """
        self._move_item(id, self.DONE_COLLECTION, self.DOING_COLLECTION)

        app.logger.debug(f"Item with id {id} marked as incomplete")

    def delete_item(self, id: str):
        """
        Deletes the item with the specified ID

        Args:
            id (str): The ID of the item.
        """

        id = ObjectId(id)
        collections = self.db.list_collection_names()

        for collection in collections:
            self.db[collection].delete_one({"_id": id})

        app.logger.debug(f"Item with id {id} deleted")

    def _as_app_item(self, item):
        return Item.from_mongo_document(item)

    def _move_item(self, id: str, from_collection: MongoCollection, to_collection: MongoCollection):
        id = ObjectId(id)

        from_db_collection = self.db[from_collection.name]
        to_db_collection = self.db[to_collection.name]

        item = from_db_collection.find_one({"_id": id})
        item['status'] = to_collection.status
        item['dateLastActivity'] = datetime.datetime.utcnow()

        to_db_collection.insert_one(item)
        from_db_collection.delete_one({"_id": id})

    # endregion

    # region user methods

    def get_or_add_user(self, user_auth_id, login, name) -> User:
        """
        If user with given auth id already exists, returns User object.
        Otherwise creates new user in database and returns corresponding User object.
        When creating a user, user is created with Admin role if no other admins exist in system,
        and as a Reader otherwise.

        Args:
            user_auth_id (str): The ID of the user from the auth system
            login (str): The login of the user for the auth system
            name (str): The name of the user from the auth system
        """
        user_collection = self.db['users']

        user_item = user_collection.find_one({"auth_id": user_auth_id})

        if user_item is None:
            return self._add_user(user_auth_id, login, name)
        else:
            return self._user_from_document(user_item)

    def get_user(self, id: str):
        """
        Retrieves the user with the specified ID as a User object

        Args:
            id (str): The ID of the user.
        """
        user_collection = self.db['users']

        user_item = user_collection.find_one({"_id": ObjectId(id)})

        return self._user_from_document(user_item)

    def get_users(self):
        """
        Fetches all users from Atlas database.

        Returns:
            list: A list of the saved items
        """
        user_collection = self.db['users']
        all_users = user_collection.find()

        users = list(map(self._user_from_document, all_users))
        return users

    def delete_user(self, id: str):
        """
        Deletes the user with the specified ID

        Args:
            id (str): The ID of the user.
        """
        collection = self.db['users']

        collection.delete_one({"_id": ObjectId(id)})

        app.logger.debug(f"User {id} deleted")

    def set_user_role(self, id: str, role: UserRole):
        """
        Updates the user with the specified ID to have the specified role

        """
        user_collection = self.db['users']

        user_document_query = {"_id": ObjectId(id)}

        user_item = user_collection.find_one(user_document_query)

        if user_item is None:
            app.logger.error(f"No user with id {id}")
            raise FileNotFoundError

        user_collection.update_one(
            user_document_query,
            {
                '$set': {'role': role.value}
            }
        )

        app.logger.debug(f"Updated user {id} to have role {role.name}")

    def _add_user(self, user_auth_id, login, name) -> User:
        user_collection = self.db['users']

        existing_admin = user_collection.find(
            {"role": "ADMIN"}).count() > 0
        role = UserRole.READER if existing_admin else UserRole.ADMIN

        user_json = {
            "auth_id": user_auth_id,
            "role": role.value,
            "login": login,
            "name": name,
        }

        user_id = user_collection.insert_one(user_json).inserted_id

        app.logger.debug(
            f"Added new user with properties {user_json} and id {user_id}")
            
        return User(user_id, user_auth_id, login, name, role)

    def _user_from_document(self, user_item):
        return User(user_item['_id'], user_item['auth_id'], user_item['login'], user_item['name'], UserRole[user_item['role']])

        # endregion

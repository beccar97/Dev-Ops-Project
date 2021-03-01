import mongomock
import re
from datetime import datetime, timedelta


class MongoClientMock:
    def __init__(self):
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()

        self.todo_item_json = {
            "name": 'TO DO ITEM',
            "status": 'To Do',
            "dateLastActivity": yesterday
        }
        self.doing_item_json = {
            "name": 'DOING ITEM',
            "status": 'Doing',
            "dateLastActivity": yesterday
        }
        self.done_item_json = {
            "name": 'DONE ITEM',
            "status": 'Done',
            "dateLastActivity": yesterday
        }

    def mock_mongo_client(self, mongo_connection_string):
        mongo_connection_string_regex = r'^mongodb\+srv:\/\/(?:[\w\-_]+):(?:[\w\-_]+)@(?:[\w\-_]+)\/([\w\-_]+)\?w=majority$'
        default_database = re.search(
            mongo_connection_string_regex, mongo_connection_string).group(1)

        client = mongomock.MongoClient()

        db = client[default_database]

        db['to_do'].insert_one(self.todo_item_json)
        db['doing'].insert_one(self.doing_item_json)
        db['done'].insert_one(self.done_item_json)

        return client

import os
from posix import environ

class MongoConfig:
    
    def __init__(self):
        env_connection_string = os.environ.get('MONGO_CONNECTION_STRING')

        if env_connection_string is not None:
            self.connection_string = env_connection_string.strip()
        else:
            self.user_name = os.environ.get('MONGO_USERNAME').strip()
            self.password = os.environ.get('MONGO_PASSWORD').strip()
            self.mongo_url = os.environ.get('MONGO_URL').strip()
            self.default_database = os.environ.get('MONGO_DEFAULT_DB').strip()
            self.connection_string =f"mongodb+srv://{self.user_name}:{self.password}@{self.mongo_url}/{self.default_database}?w=majority"

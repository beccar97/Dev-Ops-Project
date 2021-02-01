import os

class MongoConfig:
    
    def __init__(self):
        self.user_name = os.environ.get('MONGO_USERNAME').strip()
        self.password = os.environ.get('MONGO_PASSWORD').strip()
        self.mongo_url = os.environ.get('MONGO_URL').strip()
        self.default_database = os.environ.get('MONGO_DEFAULT_DB').strip()

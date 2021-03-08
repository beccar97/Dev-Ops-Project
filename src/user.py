from flask_login.mixins import UserMixin
from enum import Enum


class UserRole(Enum):
    READER = 'READER'
    WRITER = 'WRITER'


class User(UserMixin):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def role(self) -> UserRole:
        if self.id == '57951349':
            return UserRole.WRITER
        else:
            return UserRole.READER

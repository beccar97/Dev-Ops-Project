from flask_login.mixins import UserMixin, AnonymousUserMixin
from enum import Enum
import os


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

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        super().__init__()

    def role(self) -> UserRole:
        if os.environ.get('ANON_ID') == 'test_write_user':
            return UserRole.WRITER

        
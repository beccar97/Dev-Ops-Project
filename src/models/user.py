from flask_login.mixins import UserMixin, AnonymousUserMixin
from enum import Enum
import os


class UserRole(Enum):
    READER = 'READER'
    WRITER = 'WRITER'
    ADMIN = 'ADMIN'


WritePermissionRoles = [UserRole.WRITER, UserRole.ADMIN]

class User(UserMixin):
    def __init__(self, id, auth_id, login, name, role: UserRole):
        super().__init__()
        self.id = id
        self.auth_id = auth_id
        self.login = login
        self.name = name
        self.role = role

    def has_write_permissions(self):
        return self.role in WritePermissionRoles
        
    def is_admin(self):
        return self.role is UserRole.ADMIN

    def is_writer(self):
        return self.role is UserRole.WRITER

    @property
    def role_name(self):
        return self.role.value.lower()


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        super().__init__()        
        if os.environ.get('ANON_ID') == 'test_write_user':
            self.role = UserRole.WRITER
        elif os.environ.get('ANON_ID') == 'test_admin_user':
            self.role = UserRole.ADMIN
        else:
            self.role = UserRole.READER

    def has_write_permissions(self):
        return self.role in WritePermissionRoles

    def is_admin(self):
        return self.role is UserRole.ADMIN

    def id(self):
        'anonymous_user'

from src.models.user import UserRole


class AdminViewModel:
    def __init__(self, users):
        self._users = users

    @property
    def users(self):
        return self._users

    def get_users(self, role):
        return [user for user in self._users if user.role.value == role]

from flask_login.mixins import UserMixin

class User(UserMixin):
    def __init__(self, id) -> None:
        super().__init__()
        self.id = id
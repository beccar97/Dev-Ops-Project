from src.models.user import User, UserRole
from src.models.admin_view_model import AdminViewModel
from random import randint


def get_user(name: str, role: UserRole = UserRole.READER):
    id = randint(1, 100)
    return User(id, id, name.lower(), name, role)


def test_returns_admin_users():
    users = [
        get_user('Admin User', UserRole.ADMIN),
        get_user('Writer User', UserRole.WRITER),
        get_user('Reader User', UserRole.READER)
    ]
    view_model = AdminViewModel(users)
    admin_users = view_model.get_users('ADMIN')

    assert len(admin_users) == 1
    assert admin_users[0].role == UserRole.ADMIN


def test_returns_writer_users():
    users = [
        get_user('Admin User', UserRole.ADMIN),
        get_user('Writer User', UserRole.WRITER),
        get_user('Reader User', UserRole.READER)
    ]
    view_model = AdminViewModel(users)
    writer_users = view_model.get_users('WRITER')

    assert len(writer_users) == 1
    assert writer_users[0].role == UserRole.WRITER


def test_returns_reader_users():
    users = [
        get_user('Admin User', UserRole.ADMIN),
        get_user('Writer User', UserRole.WRITER),
        get_user('Reader User', UserRole.READER)
    ]
    view_model = AdminViewModel(users)
    reader_users = view_model.get_users('READER')

    assert len(reader_users) == 1
    assert reader_users[0].role == UserRole.READER

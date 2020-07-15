from todo_item import Item
from models.index_view_model import IndexViewModel

def get_task(status):
    return Item(1, 'task', status)

def test_returns_to_do_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    to_do_items = view_model.get_items('To Do')

    assert len(to_do_items) == 1
    assert to_do_items[0].status == 'To Do'

def test_returns_doing_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    to_do_items = view_model.get_items('Doing')

    assert len(to_do_items) == 1
    assert to_do_items[0].status == 'Doing'

def test_returns_done_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    to_do_items = view_model.get_items('Done')

    assert len(to_do_items) == 1
    assert to_do_items[0].status == 'Done'

from datetime import datetime, timedelta
from src.models.todo_item import Item
from src.models.index_view_model import IndexViewModel


def get_task(status: str, old: bool = False):
    timestamp = datetime.now() if not old else datetime.now() - timedelta(days=2)
    task_name = '%s %s task' % ('Old' if old else '', status)

    return Item(1, task_name, status, timestamp)


def get_tasks(status: str, old: bool = False, number: int = 5, ):
    tasks = []
    for _ in range(number):
        tasks.append(get_task(status, old))

    return tasks


def test_returns_to_do_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    to_do_items = view_model.get_items('To Do')

    assert len(to_do_items) == 1
    assert to_do_items[0].status == 'To Do'


def test_returns_doing_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    doing_items = view_model.get_items('Doing')

    assert len(doing_items) == 1
    assert doing_items[0].status == 'Doing'


def test_returns_done_items():
    items = [get_task('To Do'), get_task('Doing'), get_task('Done')]
    view_model = IndexViewModel(items)
    done_items = view_model.get_items('Done')

    assert len(done_items) == 1
    assert done_items[0].status == 'Done'


def test_returns_recent_items():
    items = get_tasks('Done') + get_tasks('Done', old=True)
    view_model = IndexViewModel(items)

    recent_done_items = view_model.recent_done_items()

    assert len(recent_done_items) == 5


def test_returns_old_items():
    items = get_tasks('Done') + get_tasks('Done', old=True, number=6)
    view_model = IndexViewModel(items)

    older_done_items = view_model.older_done_items()

    assert len(older_done_items) == 6


def test_show_all_done_items_true_when_fewer_than_five_tasks_completed():
    items = get_tasks('Done', number=3)
    view_model = IndexViewModel(items)

    assert view_model.show_all_done_items() == True


def test_show_all_done_items_true_when_exactly_five_tasks_completed():
    items = get_tasks('Done', number=5)
    view_model = IndexViewModel(items)

    assert view_model.show_all_done_items() == True


def test_show_all_done_items_false_when_more_than_five_tasks_completed():
    items = get_tasks('Done', number=7)
    view_model = IndexViewModel(items)

    assert view_model.show_all_done_items() == False

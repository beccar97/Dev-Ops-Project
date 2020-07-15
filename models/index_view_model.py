class IndexViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def get_items(self, status):
        return [item for item in self._items if item.status == status]
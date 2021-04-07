class IndexViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def get_items(self, status):
        return [item for item in self._items if item.status == status]

    def show_all_done_items(self) -> bool:
        return len(self.get_items('Done')) <=5

    def recent_done_items(self):
        return [item for item in self.get_items('Done') if item.completedToday()]

    def older_done_items(self):
        return [item for item in self.get_items('Done') if not item.completedToday()]
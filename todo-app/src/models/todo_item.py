from dateutil.parser import parse
from datetime import datetime
class Item:
    def __init__(self, id, name, status = 'To Do', dateLastActivity = datetime.now()):
        self.id = id
        self.name = name
        self.status = status
        self.dateLastActivity = dateLastActivity

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'], parse(card['dateLastActivity']))

    def dateLastActivityString(self): 
        return datetime.strftime(self.dateLastActivity, "%a %-d %b")

    def reset(self):
        self.status = 'To Do'

    def start(self):
        self.status = 'Doing'

    def complete(self):
        self.status = 'Done'

    def completedToday(self):
        return self.dateLastActivity.day == datetime.now().day
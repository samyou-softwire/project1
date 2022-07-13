from datetime import datetime

from dateutil import parser as dateparser


class Task:
    def __init__(self, id: str, title: str, status: str, description: str, due: datetime | None):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.due = due

    @staticmethod
    def from_card(card, status):
        due_str = card['due']
        if due_str is None:
            due = None
        else:
            due = dateparser.parse(due_str)

        return Task(card['id'], card['name'], status, card['desc'], due)

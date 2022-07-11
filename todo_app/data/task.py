class Task:
    def __init__(self, id: str, title: str, status: str):
        self.id = id
        self.title = title
        self.status = status

    @staticmethod
    def from_card(card, status):
        return Task(card['id'], card['name'], status)

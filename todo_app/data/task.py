class Task:
    def __init__(self, id: str, title: str, status: str, description: str):
        self.id = id
        self.title = title
        self.status = status
        self.description = description

    @staticmethod
    def from_card(card, status):
        return Task(card['id'], card['name'], status, card['desc'])

from todo_app.data.task import Task


class ViewModel:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def incomplete_items(self):
        return [task for task in self.tasks if task.status == 'incomplete']

    def complete_items(self):
        return [task for task in self.tasks if task.status == 'complete']

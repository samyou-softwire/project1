from pytest import fixture

from todo_app.data.task import Task
from todo_app.data.view_model import ViewModel


@fixture
def simple_view_model():
    view_model = ViewModel([
        Task("1", "Test", "complete", "This one is done", None),
        Task("2", "Test", "incomplete", "This one is not done", None)
    ])
    return view_model


def test_complete_items(simple_view_model):
    complete_tasks = simple_view_model.complete_items()

    assert all(task.status == "complete" for task in complete_tasks)

    # subtract complete tasks from tasks to get the rest of the tasks
    incomplete_tasks = [task for task in simple_view_model.tasks if task not in complete_tasks]

    # so every other task should have status incomplete
    assert all(task.status == "incomplete" for task in incomplete_tasks)

from typing import Callable

from pytest import fixture, mark

from todo_app.data.task import Task
from todo_app.data.view_model import ViewModel


@fixture
def simple_view_model():
    view_model = ViewModel([
        Task("1", "Test", "complete", "This one is done", None),
        Task("2", "Test", "incomplete", "This one is not done", None)
    ])
    return view_model


test_params = [
    (ViewModel.complete_items,   "complete",   "incomplete"),
    (ViewModel.incomplete_items, "incomplete", "complete")
]


@mark.parametrize("get_tasks, expected, rest", test_params)
def test_items_status(simple_view_model, get_tasks: Callable[[ViewModel], list[Task]], expected: str, rest: str):
    tasks = get_tasks(simple_view_model)

    assert all(task.status == expected for task in tasks)

    # subtract complete tasks from tasks to get the rest of the tasks
    other_tasks = [task for task in simple_view_model.tasks if task not in tasks]

    # so every other task should have status incomplete
    assert all(task.status == rest for task in other_tasks)

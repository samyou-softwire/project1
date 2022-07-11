from os import getenv
from typing import List

from requests import get, post, delete, put

from todo_app.data.task import Task

BOARD_ID = getenv("BOARD_ID")

BOARD_LISTS_URL = "https://api.trello.com/1/boards/{id}/lists"
LIST_CARDS_URL = "https://api.trello.com/1/lists/{id}/cards"
CARD_URL = "https://api.trello.com/1/cards/{id}"
CARDS_URL = "https://api.trello.com/1/cards"

DEFAULT_PARAMS = {
    'key': getenv("TRELLO_KEY"),
    'token': getenv("TRELLO_TOKEN")
}


def toggle(status):
    match status:
        case "complete":
            return "incomplete"
        case "incomplete":
            return "complete"


def get_list_ids():
    response = get(BOARD_LISTS_URL.format(id=BOARD_ID), params=DEFAULT_PARAMS).json()
    # TODO: if None, create the list
    todo_id = next((list['id'] for list in response if list['name'] == "To Do"), None)
    done_id = next((list['id'] for list in response if list['name'] == "Done"), None)

    return todo_id, done_id


def get_tasks_from_list(id, status):
    response = get(LIST_CARDS_URL.format(id=id), params=DEFAULT_PARAMS).json()

    return [Task.from_card(card, status) for card in response]


def get_tasks() -> List[Task]:
    """
    Fetches all saved tasks from the session.

    Returns:
        list: The list of saved tasks.
    """

    todo_list_id, done_list_id = get_list_ids()

    return [*get_tasks_from_list(todo_list_id, "incomplete"), *get_tasks_from_list(done_list_id, "complete")]


def get_task(id) -> Task | None:
    """
    Fetches the saved task with the specified ID.

    Args:
        id: The ID of the task.

    Returns:
        task: The saved task, or None if no tasks match the specified ID.
    """
    tasks = get_tasks()
    return next((task for task in tasks if task.id == id), None)


def add_task(title):
    """
    Adds a new task with the specified title to the session.

    Args:
        title: The title of the task.

    Returns:
        task: The saved task.
    """

    todo_list_id, _ = get_list_ids()

    add_params = {
        **DEFAULT_PARAMS,
        'idList': todo_list_id,
        'name': title
    }

    response = post(CARDS_URL, params=add_params).json()

    return Task.from_card(response, "incomplete")


def delete_task(id):
    """
    Deletes an task by its ID

    Args:
        id: The ID of the task.
    """

    delete(CARD_URL.format(id=id), params=DEFAULT_PARAMS)


def save_task(task: Task):
    """
    Updates an existing task in the session. If no existing task matches the ID of the specified task, nothing is saved.

    Args:
        task: The task to save.
    """

    todo_list_id, done_list_id = get_list_ids()

    list_id = done_list_id if task.status == "complete" else todo_list_id

    update_params = {
        **DEFAULT_PARAMS,
        'name': task.title,
        'idList': list_id
    }

    put(CARD_URL.format(id=task.id), params=update_params)

    return task

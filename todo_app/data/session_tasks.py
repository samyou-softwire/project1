from json import JSONDecodeError
from os import getenv
from typing import List

from requests import get, post, delete, put

from todo_app.data.task import Task

BOARD_ID = getenv("BOARD_ID")

BASE_URL = "https://api.trello.com/1/"

BOARD_URL = "%s/boards/{id}" % BASE_URL
BOARD_LISTS_URL = "%s/boards/{id}/lists" % BASE_URL
LISTS_URL = "%s/lists" % BASE_URL
LIST_CARDS_URL = "%s/lists/{id}/cards" % BASE_URL
CARD_URL = "%s/cards/{id}" % BASE_URL
CARDS_URL = "%s/cards" % BASE_URL

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


def get_or_create_list(name):
    response = get(BOARD_LISTS_URL.format(id=BOARD_ID), params=DEFAULT_PARAMS).json()

    id = next((list['id'] for list in response if list['name'] == name), None)

    # if this is ie a new board without the list made yet
    if id is None:
        create_list_params = {
            **DEFAULT_PARAMS,
            'name': name,
            'idBoard': get_long_board_id()
        }

        response = post(LISTS_URL, params=create_list_params).json()
        return response["id"]
    else:
        return id


def get_list_ids():
    todo_id = get_or_create_list("To Do")
    done_id = get_or_create_list("Done")

    return todo_id, done_id


# lazy loads the long board id
_long_board_id = None


def get_long_board_id():
    global _long_board_id

    if _long_board_id is None:
        response = get(BOARD_URL.format(id=BOARD_ID), params=DEFAULT_PARAMS).json()
        _long_board_id = response["id"]

    return _long_board_id


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

    try:
        response = get(CARD_URL.format(id=id), params=DEFAULT_PARAMS).json()
    except JSONDecodeError:
        return None

    todo_list_id, done_list_id = get_list_ids()

    if response['idList'] == done_list_id:
        status = "complete"
    else:
        status = "incomplete"

    return Task.from_card(response, status)


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
        'idList': list_id,
        'desc': task.description,
        'due': task.due.strftime("%Y-%m-%dT%H:%M:%S") if task.due is not None else ""
    }

    put(CARD_URL.format(id=task.id), params=update_params)

    return task

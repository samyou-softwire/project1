from os import getenv

from flask import session
from requests import get

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'incomplete', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'incomplete', 'title': 'Allow new items to be added' }
]

BOARD_ID = getenv("BOARD_ID")

LISTS_ON_BOARD_URL = "https://api.trello.com/1/boards/{id}/lists"
CARDS_ON_LIST_URL = "https://api.trello.com/1/lists/{id}/cards"

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
    response = get(LISTS_ON_BOARD_URL.format(id=BOARD_ID), params=DEFAULT_PARAMS).json()
    # TODO: if None, create the list
    todo_id = next((list['id'] for list in response if list['name'] == "To Do"), None)
    done_id = next((list['id'] for list in response if list['name'] == "Done"), None)

    return todo_id, done_id


def get_tasks_from_list(id, status):
    response = get(CARDS_ON_LIST_URL.format(id=id), params=DEFAULT_PARAMS).json()

    return [{
        'id': item["id"],
        'status': status,
        'title': item["name"]
    } for item in response]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    todo_list_id, done_list_id = get_list_ids()

    return [*get_tasks_from_list(todo_list_id, "incomplete"), *get_tasks_from_list(done_list_id, "complete")]


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'incomplete' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def delete_item(id):
    """
    Deletes an item by its ID

    Args:
        id: The ID of the item.
    """
    session['items'] = [item for item in session['items'] if item['id'] != id]


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item


def reset_items():
    """
    Sets current session items back to the default
    """

    session.pop('items')

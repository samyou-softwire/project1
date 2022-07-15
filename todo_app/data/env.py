from os import getenv


def get_board_id():
    return getenv("BOARD_ID")


def get_organization_id():
    return getenv("ORGANIZATION_ID")


def get_default_params():
    return {
        'key': getenv("TRELLO_KEY"),
        'token': getenv("TRELLO_TOKEN")
    }
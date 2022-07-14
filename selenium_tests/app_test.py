from os import environ
from threading import Thread
from time import sleep

from _pytest.monkeypatch import MonkeyPatch
from requests import post, delete
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from todo_app import app

import pytest

from todo_app.data import session_tasks


def create_test_board():
    from todo_app.data.session_tasks import ORGANIZATION_ID, BOARDS_URL, DEFAULT_PARAMS

    create_params = {
        **DEFAULT_PARAMS,
        'idOrganization': ORGANIZATION_ID,
        'defaultLists': "false",
        'name': "TEST"
    }

    response = post(BOARDS_URL, params=create_params).json()

    return response['id']


def delete_test_board(id):
    from todo_app.data.session_tasks import BOARD_URL, DEFAULT_PARAMS

    delete(BOARD_URL.format(id=id), params=DEFAULT_PARAMS)


@pytest.fixture(scope='module')
def app_with_temp_board():
    with MonkeyPatch().context() as monkeypatch:
        session_tasks.init_env()

        board_id = create_test_board()

        monkeypatch.setattr(session_tasks, "BOARD_ID", board_id)
        monkeypatch.setattr(session_tasks, "init_env", lambda: None)
        environ["BOARD_ID"] = board_id

        thread = Thread(target=lambda: todo_app.run(use_reloader=False))

        todo_app = app.create_app()

        print(session_tasks.BOARD_ID)
        print(board_id)

        thread.daemon = True
        thread.start()

        sleep(1)

        yield todo_app

        thread.join(1)

        delete_test_board(board_id)


@pytest.fixture(scope='module')
def driver():
    with webdriver.Edge(EdgeChromiumDriverManager().install()) as driver:
        yield driver


def test_app_loads(driver, app_with_temp_board):
    driver.get("http://localhost:5000")

    assert driver.title == 'To-Do App'

from os import environ
from threading import Thread
from time import sleep

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from todo_app import app

import pytest


@pytest.fixture(scope='module')
def app_with_temp_board():
    # board_id = "abcd"
    # environ['BOARD_ID'] = board_id

    todo_app = app.create_app()

    thread = Thread(target=lambda: todo_app.run(use_reloader=False))

    thread.daemon = True
    thread.start()

    sleep(1)

    yield todo_app

    thread.join(1)
    # delete trello board?


@pytest.fixture(scope='module')
def driver():
    with webdriver.Edge(EdgeChromiumDriverManager().install()) as driver:
        yield driver


def test_app_loads(driver, app_with_temp_board):
    driver.get("http://localhost:5000")

    assert driver.title == 'To-Do App'

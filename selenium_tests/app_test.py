from os import environ
from threading import Thread
from time import sleep

from _pytest.monkeypatch import MonkeyPatch
from requests import post, delete
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from todo_app import app

import pytest

from todo_app.data import session_tasks
from todo_app.data.env import get_default_params, get_organization_id, get_board_id
from todo_app.data.session_tasks import BOARD_URL, BOARDS_URL, toggle


def create_test_board():
    create_params = {
        **get_default_params(),
        'idOrganization': get_organization_id(),
        'defaultLists': "false",
        'name': "TEST"
    }

    response = post(BOARDS_URL, params=create_params).json()

    return response['id']


def delete_test_board(id):
    delete(BOARD_URL.format(id=id), params=get_default_params())


@pytest.fixture(scope='module')
def app_with_temp_board():
    board_id = create_test_board()

    environ["BOARD_ID"] = board_id

    thread = Thread(target=lambda: todo_app.run(use_reloader=False))

    todo_app = app.create_app()

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


def add_task(name, driver):
    add_name = driver.find_element(By.ID, "itemtitle")
    add_name.send_keys(name)
    add_button = driver.find_element(By.ID, "btn-add")
    add_button.click()


def find_action_button(name, driver, button_name):
    label = driver.find_element(By.NAME, name)
    parent: WebElement = label.find_element(By.XPATH, "./..")
    button = parent.find_element(By.NAME, button_name)
    return button


def task_is(status, name, driver):
    wanted_list = driver.find_element(By.ID, status)
    unwanted_list = driver.find_element(By.ID, toggle(status))
    assert wanted_list.find_elements(By.NAME, name)
    assert not unwanted_list.find_elements(By.NAME, name)


@pytest.mark.skip
def test_app_loads(driver, app_with_temp_board):
    driver.get("http://localhost:5000")

    assert driver.title == 'To-Do App'


@pytest.mark.skip
def test_add_element(driver, app_with_temp_board):
    driver.get("http://localhost:5000")

    add_task("This is a hard task", driver)

    assert "This is a hard task" in driver.page_source


@pytest.mark.skip
def test_delete_element(driver, app_with_temp_board):
    delete_me = "Please delete this task"

    driver.get("http://localhost:5000")

    add_task(delete_me, driver)

    assert delete_me in driver.page_source

    button = find_action_button(delete_me, driver, "delete")
    button.click()

    assert delete_me not in driver.page_source


@pytest.mark.skip
def test_delete_element_with_others_on_page(driver, app_with_temp_board):
    dont_delete_me = "Please DO NOT delete this task"
    delete_me = "Please delete this task"
    dont_delete_me2 = "Also please DO NOT delete this task either"

    driver.get("http://localhost:5000")

    add_task(delete_me, driver)
    add_task(dont_delete_me, driver)
    add_task(dont_delete_me2, driver)

    assert delete_me in driver.page_source
    assert dont_delete_me in driver.page_source
    assert dont_delete_me2 in driver.page_source

    button = find_action_button(delete_me, driver, "delete")
    button.click()

    assert delete_me not in driver.page_source
    assert dont_delete_me in driver.page_source
    assert dont_delete_me2 in driver.page_source


@pytest.mark.skip
def test_new_task_goes_to_incomplete(driver, app_with_temp_board):
    this_is_a_new_incomplete_task = "This is a new incomplete task"

    driver.get("http://localhost:5000")

    add_task(this_is_a_new_incomplete_task, driver)

    task_is("incomplete", this_is_a_new_incomplete_task, driver)


@pytest.mark.skip
def test_switching_between_tasks(driver, app_with_temp_board):
    this_is_an_incomplete_task = "This is an incomplete task"

    driver.get("http://localhost:5000")

    add_task(this_is_an_incomplete_task, driver)

    task_is("incomplete", this_is_an_incomplete_task, driver)

    change_status_button = find_action_button(this_is_an_incomplete_task, driver, "changestatus")
    change_status_button.click()

    task_is("complete", this_is_an_incomplete_task, driver)


def test_adding_description(driver, app_with_temp_board):
    rename_me = "Rename me"
    new_description = "New description"

    driver.get("http://localhost:5000")

    add_task(rename_me, driver)

    edit_button = find_action_button(rename_me, driver, "edit")
    edit_button.click()

    description_box = find_action_button(rename_me, driver, "description")
    description_box.send_keys(new_description)

    submit_button = find_action_button(rename_me, driver, "submit")
    submit_button.click()

    assert new_description in driver.page_source

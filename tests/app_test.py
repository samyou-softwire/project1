from os import getenv
from unittest.mock import MagicMock

import requests
from pytest import fixture
from dotenv import load_dotenv, find_dotenv

from todo_app import app


@fixture
def client():
    test_env = find_dotenv(".env.test")
    load_dotenv(test_env, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


TEST_LISTS = [
    {
        'id': "1",
        'name': "To Do"
    },
    {
        'id': "2",
        'name': "Done"
    }
]
TEST_TASKS = [
    {
        'id': "1",
        'name': "Task 1",
        'due': None,
        'desc': "Complete me",
        'idList': "1"
    }
]

class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def get_stub(url, params):
    board_id = getenv('BOARD_ID')

    # must be imported now else it'll have None value its initialised with
    from todo_app.data.session_tasks import BOARD_LISTS_URL
    if url == BOARD_LISTS_URL.format(id=board_id):
        return StubResponse(TEST_LISTS)

    from todo_app.data.session_tasks import LIST_CARDS_URL

    for list in TEST_LISTS:
        if url == LIST_CARDS_URL.format(id=list['id']):
            return StubResponse([task for task in TEST_TASKS if task['idList'] == list['id']])

    raise Exception(f"Unknown URL {url}")


def post_stub(url, params):
    return StubResponse(TEST_TASKS[0])


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_stub)

    response = client.get("/")

    assert response.status_code == 200
    assert "Task 1" in response.data.decode()
    assert "Complete me" in response.data.decode()


def test_add(mocker, monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_stub)
    monkeypatch.setattr(requests, 'post', post_stub)
    spy: MagicMock = mocker.spy(requests, "post")

    client.post("/add")

    assert spy.call_count == 1

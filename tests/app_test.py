from os import getenv

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


def stub(url, params):
    board_id = getenv('BOARD_ID')

    class StubResponse:
        def __init__(self, fake_response_data):
            self.fake_response_data = fake_response_data

        def json(self):
            return self.fake_response_data

    # must be imported now else it'll have None value its initialised with
    from todo_app.data.session_tasks import BOARD_LISTS_URL
    if url == BOARD_LISTS_URL.format(id=board_id):
        return StubResponse([
            {
                'id': "1",
                'name': "To Do"
            },
            {
                'id': "2",
                'name': "Done"
            }
        ])

    from todo_app.data.session_tasks import LIST_CARDS_URL
    if url in [LIST_CARDS_URL.format(id="1"), LIST_CARDS_URL.format(id="2")]:
        return StubResponse([{
            'id': "1",
            'name': "Task 1",
            'due': None,
            'desc': "Complete me"
        }])

    raise Exception(f"Unknown URL {url}")


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get("/")

    assert response.status_code == 200
    assert "Task 1" in response.data.decode()
    assert "Complete me" in response.data.decode()


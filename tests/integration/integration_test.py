import pytest
import pymongo
import src.app as app
from dotenv import find_dotenv, load_dotenv
from tests.mongo_client_mock import MongoClientMock


@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    mock_mongo_client = MongoClientMock().mock_mongo_client
    monkeypatch.setattr(pymongo, "MongoClient", mock_mongo_client)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(client):

    response = client.get('/')
    htmlResponse = response.data.decode("utf-8")

    assert "TO DO ITEM" in htmlResponse
    assert "DOING ITEM" in htmlResponse
    assert "DONE ITEM" in htmlResponse

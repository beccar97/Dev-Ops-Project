import pytest
import requests
import app
import os
from dotenv import find_dotenv, load_dotenv
from request_get_mock import mock_get_requests

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", mock_get_requests)

    response = client.get('/')
    htmlResponse = response.data.decode("utf-8")

    assert "TO DO ITEM" in htmlResponse
    assert "DOING ITEM" in htmlResponse
    assert "DONE ITEM" in htmlResponse
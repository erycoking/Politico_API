import pytest
import unittest
from politico import create_app
from politico.api.v2.db import DB


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    app.config['TESTING'] = True
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    db = DB()
    yield test_client
    db.tear_down_test_database()
    ctx.pop()


def standard(response):
    data = response.get_json()
    assert 'data' in data
    assert 'status' in data
    return data


def error_standard(response):
    data = response.get_json()
    assert 'error' in data
    assert 'status' in data
    return data



@pytest.fixture(scope='module')
def token(test_client):
    login_credentials = dict(
        username='pheonix',
        password='admin123'
    )
    response = test_client.post('/api/v2/auth/login', json = login_credentials)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'token' in data[0]
    token = data[0]['token']
    assert token is not None
    return token




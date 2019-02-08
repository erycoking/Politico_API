""" A test for testing user routes"""

"""imports core modules """
import pytest

"""import custom modules"""
from .....config import create_app

prefix = '/api/v1'

@pytest.fixture(scope = 'module')
def test_client():
    """A fixture for creating a test_client"""
    test_client = create_app().test_client()
    cxt = create_app().app_context()
    cxt.push()

    yield test_client

    cxt.pop()


def add_user(test_client):
    user_data = {
        "email": "eryco@gmail.com",
        "firstname": "king",
        "id_no": "12345608",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "",
        "passport_url": "file/passports/passport1.png",
        "phone_number": "0712345678", 
        "username":"baller",
        "password":"password"
    }
    return test_client.post(prefix+'/users', json=user_data)

def update_user(test_client):
    user_data = {
        "email": "eryco@gmail.com",
        "firstname": "bigfish",
        "id_no": "12345608",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "",
        "passport_url": "file/passports/passport1.png",
        "phone_number": "0712345678",
        "username":"baller",
        "password":"password"
    }
    return test_client.patch(prefix+'/users/1', json=user_data)


def test_add_user(test_client):
    """A test for adding a user"""
    with test_client as c:
        response = add_user(c)
        assert response.status_code == 201
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'full_name' in data['data'][0] and data['data'][0]['full_name'] == 'king rozay'

def test_get_single_user(test_client):
    """A test for getting a single user"""
    with test_client as c:
        add_user(c)
        response = c.get(prefix+'/users/1')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'firstname' in data['data'][0] and data['data'][0]['firstname'] == 'king'

def test_update_user(test_client):
    """A test for getting a single user"""
    with test_client as c:
        response = update_user(c)
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'full_name' in data['data'][0] and data['data'][0]['full_name'] == 'bigfish rozay'

def test_getting_all_users(test_client):
    """A test for getting all user"""
    with test_client as c:
        add_user(c)
        response = c.get(prefix+'/users')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'firstname' in data['data'][0] and data['data'][0]['firstname'] == 'bigfish'

def test_delete_user(test_client):
    """A test for deleting a single user"""
    with test_client as c:
        add_user(c)
        response = c.delete(prefix+'/users/1')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'message' in data['data'] and data['data']['message'] == 'user successfully deleted'

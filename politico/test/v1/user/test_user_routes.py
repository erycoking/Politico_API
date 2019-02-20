import pytest
from ...base import test_client

prefix = '/api/v1'


def add_user(test_client):
    user_data = {
        "email": "loningo@gmail.com",
        "firstname": "king",
        "id_no": "123456080",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "king",
        "passport_url": "http://file.com/passports/passport1.png",
        "phone_number": "0712340000",
        "username": "baller1",
        "password": "password"
    }
    return test_client.post(prefix+'/users', json=user_data)


def update_user(test_client):
    user_data = {
        "email": "lomunyak@gmail.com",
        "firstname": "bigfish",
        "id_no": "12345608",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "king",
        "passport_url": "http://file.com/passports/passport1.png",
        "phone_number": "0712345679",
        "username": "baller675",
        "password": "password"
    }
    return test_client.patch(prefix+'/users/1', json=user_data)


def test_add_user(test_client):
    """A test for adding a user"""
    response = add_user(test_client)
    assert response.status_code == 201
    data = response.get_json()
    assert 'data' in data
    user = data.get('data')[0]
    print(user)
    assert 'id' in user and user['id'] == 1
    assert 'firstname' in user and user['firstname'] == 'king'


def test_get_single_user(test_client):
    """A test for getting a single user"""
    add_user(test_client)
    response = test_client.get(prefix+'/users/1')
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert 'data' in data
    user = data.get('data')[0]
    assert 'id' in user and user['id'] == 1
    assert 'firstname' in user and user['firstname'] == 'king'


def test_update_user(test_client):
    """A test for getting a single user"""
    response = update_user(test_client)
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert 'data' in data
    user = data.get('data')[0]
    assert 'id' in user and user['id'] == 1
    assert 'firstname' in user and user['firstname'] == 'bigfish'


def test_getting_all_users(test_client):
    """A test for getting all user"""
    add_user(test_client)
    response = test_client.get(prefix+'/users')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    users = data.get('data')
    first_user = users.get('1')
    print(users)
    assert 'id' in first_user and first_user['id'] == 1
    assert 'firstname' in first_user and first_user['firstname'] == 'king'


def test_delete_user(test_client):
    """A test for deleting a single user"""
    add_user(test_client)
    response = test_client.delete(prefix+'/users/1')
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert 'data' in data
    assert 'message' in data['data'] and data['data']['message'] == 'user successfully deleted'

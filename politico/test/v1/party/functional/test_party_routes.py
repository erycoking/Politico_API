"""tests for testing party routes"""

# importing core modules
import pytest

# importing custom modules
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

def add_party(test_client):
    party_data = {
        "hq_address": "Westlands, Nairobi",
        "logo_url": "logo/logo.jpg",
        "name": "jubilee"
    }
    return test_client.post(prefix+'/parties', json=party_data)

def update_party(test_client):
    party_data = {
        "hq_address": "Thika road, Nairobi",
        "logo_url": "logo/logo.jpg",
        "name": "jubilee"
    }
    return test_client.patch(prefix+'/parties/1', json=party_data)


def test_add_party(test_client):
    """A test for adding a party"""
    with test_client as c:
        response = add_party(c)
        assert response.status_code == 201
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'name' in data['data'][0] and data['data'][0]['name'] == 'jubilee'

def test_get_single_party(test_client):
    """A test for getting a single party"""
    with test_client as c:
        add_party(c)
        response = c.get(prefix+'/parties/1')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'name' in data['data'][0] and data['data'][0]['name'] == 'jubilee'

def test_update_party(test_client):
    """A test for getting a single party"""
    with test_client as c:
        response = update_party(c)
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'name' in data['data'][0] and data['data'][0]['name'] == 'jubilee'

def test_getting_all_partys(test_client):
    """A test for getting all party"""
    with test_client as c:
        add_party(c)
        response = c.get(prefix+'/parties')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'id' in data['data'][0] and data['data'][0]['id'] == 1
        assert 'name' in data['data'][0] and data['data'][0]['name'] == 'jubilee'

def test_delete_party(test_client):
    """A test for deleting a single party"""
    with test_client as c:
        add_party(c)
        response = c.delete(prefix+'/parties/1')
        assert response.status_code == 200
        data  = response.get_json()
        print(data)
        assert 'data' in data
        assert 'message' in data['data'] and data['data']['message'] == 'Party successfully deleted'

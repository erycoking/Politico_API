"""test cases for office routes"""

# import core module
import pytest

# import custom modules
from .....config import create_app

# prefix
prefix = '/api/v1'

@pytest.fixture(scope='module')
def test_client():
    # initializing the test client
    test_client = create_app().test_client()
    ctx = create_app().app_context()
    ctx.push()
    yield test_client
    ctx.pop()

def create_office(test_client):
    # creates office
    office_data = {
        "type": "local_government",
        "name": "governer"
    }
    return test_client.post(prefix+'/offices', json = office_data)

def update_office(test_client):
    # update office
    update_data = {
            "type": "local_government", 
            "name": "woman rep"
        }
    return test_client.patch(prefix+'/offices/1', json = update_data)

def test_add_office_route(test_client):
    # tests the create office route
    with test_client as client:
        office_resp = create_office(client)
        assert office_resp.status_code == 201
        resp = office_resp.get_json()
        assert resp is not None
        assert resp['data'][0]['name'] == 'governer'
        assert resp['data'][0]['type'] == 'local_government'
        assert resp['data'][0]['type'] in ['federal', 'legislative', 'state', 'local_government']


def test_get_all_offices(test_client):
    # tests getting all offices route
    with test_client as client:
        create_office(client)
        res = client.get(prefix+'/offices')
        assert res.status_code == 200
        res_data = res.get_json()
        assert len(res_data['data']) == 1
        assert res_data['data'][0]['id'] == 1

def test_get_single_office(test_client):
    # tests getting a single office route
    with test_client as client:
        create_office(client)
        rs = client.get(prefix+'/offices/1')
        assert rs.status_code == 200
        rs_data = rs.get_json()
        assert len(rs_data['data']) == 1
        assert rs_data['data'][0]['id'] == 1
        assert rs_data['data'][0]['name'] == 'governer'

def test_update_office(test_client):
    # test update office route
    with test_client as client:
        rs = update_office(client)
        assert rs.status_code == 200
        rs_data = rs.get_json()
        assert rs_data['data'][0]['name'] == 'woman rep'
        assert rs_data['data'][0]['type'] == 'local_government'
        assert rs_data['data'][0]['type'] in ['federal', 'legislative', 'state', 'local_government']

def test_delete_office(test_client):
    # tests delete office route
    with test_client as client:
        create_office(client)
        rs  = client.delete(prefix+'/offices/1')
        assert rs.status_code == 200
        rs_data = rs.get_json()
        assert rs_data['data'][0]['message'] == 'office with id:1 deleted'

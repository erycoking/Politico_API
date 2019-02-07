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
    ctx.push
    yield test_client
    ctx.pop

def create_office(test_client):
    office_data = {
        "type": "local_government",
        "name": "governer"
    }
    return test_client.post(prefix+'/offices', json = office_data)

def test_add_office_route(test_client):
    with test_client as client:
        office_resp = create_office(client)
        assert office_resp is not None

def test_get_all_offices(test_client):
    with test_client as client:
        create_office(client)
        res = client.get(prefix+'/offices')
        res_data = res.get_json()
        assert len(res_data['data']) == 1


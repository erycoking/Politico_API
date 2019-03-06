import pytest
from ...base import test_client, token, standard, error_standard

@pytest.fixture(scope='module')
def office():
    office = {
        "type": "local government", 
        "name": "senetor"
    }
    return office

@pytest.fixture(scope='module')
def office_2():
    office = {
        "type": "local government", 
        "name": "mca"
    }
    return office

@pytest.fixture(scope='module')
def bad_office():
    office = {
        "type": "", 
        "name": "senetor"
    }
    return office

@pytest.fixture(scope='module')
def bad_office_2():
    office = {
        "type": "local government", 
        "name": "senetor123"
    }
    return office

def test_add_office(test_client, token, office):
    url = '/api/v2/offices'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=office)
    assert response.status_code == 201
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    office_1 = data[0]
    assert 'type' in office_1 and office_1['type'] == 'local government'
    assert 'name' in office_1 and office_1['name'] == 'senetor'

def test_add_bad_office(test_client, token, bad_office):
    url = '/api/v2/offices'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_office)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'Invalid office type.'


def test_add_bad_office_2(test_client, token, bad_office_2):
    url = '/api/v2/offices'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_office_2)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'Invalid office name. Office name should be made of alphabets only'

def test_upate_office(test_client, token, office_2):
    url = '/api/v2/offices/1'
    response  = test_client.open(url, method='PATCH', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=office_2)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    office = data[0]
    assert 'type' in office and office['type'] == 'local government'
    assert 'name' in office and office['name'] == 'mca'

def test_get_all_offices(test_client, token):
    url = '/api/v2/offices'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    office_1 = data[0]
    assert office_1 is not None
    assert 'name' in office_1 and office_1['name'] == 'mca'
    assert 'type' in office_1 and office_1['type'] == 'local government'

def test_get_single_office(test_client, token):
    url = '/api/v2/offices/1'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    office_1 = data[0]
    assert office_1 is not None
    assert 'name' in office_1 and office_1['name'] == 'mca'
    assert 'type' in office_1 and office_1['type'] == 'local government'

def test_delete_office(test_client, token):
    url = '/api/v2/offices/1'
    response = test_client.open(url, method='DELETE', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'message' in data[0]
    assert data[0]['message'] == 'office with id:1 deleted'
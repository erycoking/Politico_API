import pytest
from ...base import test_client, token, standard, error_standard

@pytest.fixture(scope='module')
def party():
    party = {
        "hq_address": "Westlands, Nairobi.",
        "logo_url": "http://logo.com/logo/logo.jpg",
        "name": "Nasa ria"
    }
    return party

@pytest.fixture(scope='module')
def party_2():
    party = {
        "hq_address": "Thika road, Nairobi.",
        "logo_url": "http://logo.com/logo/logo.jpg",
        "name": "Nasa ria"
    }
    return party

@pytest.fixture(scope='module')
def bad_party():
    party = {
        "hq_address": "Westlands, Nairobi.",
        "logo_url": "http://logo.com/logo/logo.jpg",
        "name": ""
    }
    return party

@pytest.fixture(scope='module')
def bad_party_2():
    party = {
        "hq_address": "Westlands, Nairobi.",
        "logo_url": "http://logo/logo/logo.jpg",
        "name": "Nasa ria"
    }
    return party

def test_add_party(test_client, token, party):
    url = '/api/v2/parties'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=party)
    assert response.status_code == 201
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    party_1 = data[0]
    assert 'hq_address' in party_1 and party_1['hq_address'] == 'Westlands, Nairobi.'
    assert 'name' in party_1 and party_1['name'] == 'Nasa ria'

def test_add_bad_party(test_client, token, bad_party):
    url = '/api/v2/parties'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_party)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'Invalid name.Name should not be less than 3 characters and should contain only alphabets'


def test_add_bad_party_2(test_client, token, bad_party_2):
    url = '/api/v2/parties'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_party_2)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'Invalid logo_url.Please give a valid url'

def test_upate_party(test_client, token, party_2):
    url = '/api/v2/parties/1'
    response  = test_client.open(url, method='PATCH', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=party_2)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    party = data[0]
    assert 'hq_address' in party and party['hq_address'] == 'Thika road, Nairobi.'
    assert 'name' in party and party['name'] == 'Nasa ria'

def test_get_all_parties(test_client, token):
    url = '/api/v2/parties'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    party_1 = data[0]
    assert party_1 is not None
    assert 'name' in party_1 and party_1['name'] == 'Nasa ria'
    assert 'hq_address' in party_1 and party_1['hq_address'] == 'Thika road, Nairobi.'

def test_get_single_party(test_client, token):
    url = '/api/v2/parties/1'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    party_1 = data[0]
    assert party_1 is not None
    assert 'name' in party_1 and party_1['name'] == 'Nasa ria'
    assert 'hq_address' in party_1 and party_1['hq_address'] == 'Thika road, Nairobi.'

def test_delete_party(test_client, token):
    url = '/api/v2/parties/1'
    response = test_client.open(url, method='DELETE', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'message' in data
    assert data['message'] == 'Party successfully deleted'
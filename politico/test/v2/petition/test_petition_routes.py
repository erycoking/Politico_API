import pytest
from ...base import test_client, token, standard, error_standard

def init(test_client, token):
    
    office = {
        "type": "state", 
        "name": "president"
    }

    office_2 = {
        "type": "local government", 
        "name": "senetor"
    }

    url = '/api/v2/offices'

    response_3  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=office)

    assert response_3.status_code == 201

    response_4  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=office_2)

    assert response_4.status_code == 201

    party = {
        "hq_address": "Westlands, Nairobi.",
        "logo_url": "http://logo.com/logo/logo12.jpg",
        "name": "jubilee"
    }
    party_2 = {
        "hq_address": "Kasarani, Nairobi.",
        "logo_url": "http://logo.com/logo/logo123.jpg",
        "name": "Nasa"
    }

    url_2 = '/api/v2/parties'

    response  = test_client.open(url_2, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=party)

    assert response.status_code == 201

    response_2  = test_client.open(url_2, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=party_2)

    assert response_2.status_code == 201


@pytest.fixture(scope='module')
def petition():
    petition = {
        "office": "president", 
        "body": "election was rigged", 
        "evidence": ["evidence_1", "evidence_2"]
    }
    return petition


@pytest.fixture(scope='module')
def petition_2():
    petition = {
        "office": "president", 
        "body": "election was unfair", 
        "evidence": ["evidence_1", "evidence_2", "evidence_3"]
    }
    return petition

@pytest.fixture(scope='module')
def bad_petition():
    petition = {
        "body": "election was unfair", 
        "evidence": ["evidence_1", "evidence_2", "evidence_3"]
    }
    return petition

@pytest.fixture(scope='module')
def bad_petition_2():
    petition = {
        "office": "qwertyu",
        "body": "election was unfair", 
        "evidence": ["evidence_1", "evidence_2", "evidence_3"]
    }
    return petition

def test_add_petition(test_client, token, petition):
    init(test_client, token)

    url = '/api/v2/petitions'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=petition)
    assert response.status_code == 201
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    petition_1 = data[0]
    assert 'office' in petition_1 and petition_1['office'] == 'president'
    assert 'body' in petition_1 and petition_1['body'] == 'election was rigged'
    assert 'id' in petition_1 and petition_1['id'] == 1

def test_add_bad_petition(test_client, token, bad_petition):
    url = '/api/v2/petitions'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_petition)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'office missing'


def test_add_bad_petition_2(test_client, token, bad_petition_2):
    url = '/api/v2/petitions'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_petition_2)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'Office does not exist'

def test_update_petition(test_client, token, petition_2):
    url = '/api/v2/petitions/1'
    response  = test_client.open(url, method='PATCH', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=petition_2)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    petition_1 = data[0]
    assert 'office' in petition_1 and petition_1['office'] == 'president'
    assert 'body' in petition_1 and petition_1['body'] == 'election was unfair'
    assert 'id' in petition_1 and petition_1['id'] == 1

def test_get_all_petitions(test_client, token):
    url = '/api/v2/petitions'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    petition_1 = data[0]
    assert petition_1 is not None
    assert 'office' in petition_1 and petition_1['office'] == 'president'
    assert 'body' in petition_1 and petition_1['body'] == 'election was unfair'
    assert 'id' in petition_1 and petition_1['id'] == 1

def test_get_single_petition(test_client, token):
    url = '/api/v2/petitions/1'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    petition_1 = data[0]
    assert petition_1 is not None
    assert 'office' in petition_1 and petition_1['office'] == 'president'
    assert 'body' in petition_1 and petition_1['body'] == 'election was unfair'
    assert 'id' in petition_1 and petition_1['id'] == 1

def test_delete_petition(test_client, token):
    url = '/api/v2/petitions/1'
    response = test_client.open(url, method='DELETE', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'message' in data
    assert data['message'] == 'petition with id:1 successfully deleted'



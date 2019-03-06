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
def candidates():
    candidates = {
        "party":"jubilee"
    }
    return candidates

@pytest.fixture(scope='module')
def candidates_2():
    candidates = {
        "party":"Nasa"
    }
    return candidates

@pytest.fixture(scope='module')
def bad_candidates():
    candidates = {
    }
    return candidates

@pytest.fixture(scope='module')
def bad_candidates_2():
    candidates = candidates = {
        "party":1,
    }
    return candidates

def test_add_candidates(test_client, token, candidates):
    init(test_client, token)

    url = '/api/v2/office/1/register'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=candidates)
    assert response.status_code == 201
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    candidates_1 = data[0]
    assert 'office' in candidates_1 and candidates_1['office'] == 'president'
    assert 'party' in candidates_1 and candidates_1['party'] == 'jubilee'
    assert 'id' in candidates_1 and candidates_1['id'] == 1

def test_add_bad_candidates(test_client, token, bad_candidates):
    url = '/api/v2/office/1/register'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_candidates)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'party missing'


def test_add_bad_candidates_2(test_client, token, bad_candidates_2):
    url = '/api/v2/office/1/register'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_candidates_2)
    assert response.status_code == 500


def test_update_candidates(test_client, token, candidates_2):
    url = '/api/v2/office/1/candidates/1'
    response  = test_client.open(url, method='PATCH', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=candidates_2)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    candidates_1 = data[0]
    assert 'office' in candidates_1 and candidates_1['office'] == 'president'
    assert 'party' in candidates_1 and candidates_1['party'] == 'Nasa'
    assert 'id' in candidates_1 and candidates_1['id'] == 1

def test_get_all_candidatess(test_client, token):
    url = '/api/v2/office/1/candidates'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    candidates_1 = data[0]
    assert candidates_1 is not None
    assert 'office' in candidates_1 and candidates_1['office'] == 'president'
    assert 'party' in candidates_1 and candidates_1['party'] == 'Nasa'
    assert 'id' in candidates_1 and candidates_1['id'] == 1

def test_get_single_candidates(test_client, token):
    url = '/api/v2/office/1/candidates/1'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    candidates_1 = data[0]
    assert candidates_1 is not None
    assert 'office' in candidates_1 and candidates_1['office'] == 'president'
    assert 'party' in candidates_1 and candidates_1['party'] == 'Nasa'
    assert 'id' in candidates_1 and candidates_1['id'] == 1

def test_delete_candidates(test_client, token):
    url = '/api/v2/office/1/candidates/1'
    response = test_client.open(url, method='DELETE', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'message' in data
    assert data['message'] == 'candidates with id:1 successfully deleted'
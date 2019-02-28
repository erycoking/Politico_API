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

    candidates = {
        "party":"jubilee"
    }

    url_3 = '/api/v2/office/1/register'

    response  = test_client.open(url_3, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=candidates)

    assert response.status_code == 201

@pytest.fixture(scope='module')
def vote():
    vote = {
        "office": "president", 
        "candidate": 1
    }
    return vote


@pytest.fixture(scope='module')
def bad_vote():
    vote = {
        "office": "senetor", 
        "candidate": 10
    }
    return vote

@pytest.fixture(scope='module')
def bad_vote_2():
    vote = {
        "office": "president", 
        "candidate": 10
    }
    return vote

def test_add_vote(test_client, token, vote):
    init(test_client, token)

    url = '/api/v2/votes'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=vote)
    assert response.status_code == 201
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    vote_1 = data[0]
    assert 'office' in vote_1 and vote_1['office'] == 'president'
    assert 'candidate' in vote_1 and vote_1['candidate'] == 'Erick'
    assert 'created_by' in vote_1 and vote_1['created_by'] == 'Erick'
    assert 'id' in vote_1 and vote_1['id'] == 1

def test_add_bad_vote(test_client, token, bad_vote):
    url = '/api/v2/votes'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_vote)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'No candidate by name::10 is running for office by name::senetor'


def test_add_bad_vote_2(test_client, token, bad_vote_2):
    url = '/api/v2/votes'
    response  = test_client.open(url, method='POST', headers={
        'Authorization': 'Bearer {}'.format(token)
    }, json=bad_vote_2)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'No candidate by name::10 is running for office by name::president'


def test_get_all_votes(test_client, token):
    url = '/api/v2/votes'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    vote_1 = data[0]
    assert vote_1 is not None
    assert 'office' in vote_1 and vote_1['office'] == 'president'
    assert 'candidate' in vote_1 and vote_1['candidate'] == 'Erick'
    assert 'created_by' in vote_1 and vote_1['created_by'] == 'Erick'
    assert 'id' in vote_1 and vote_1['id'] == 1

def test_get_single_vote(test_client, token):
    url = '/api/v2/offices/1/result'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    vote_1 = data[0]
    assert vote_1 is not None
    assert 'office' in vote_1 and vote_1['office'] == 'president'
    assert 'candidate' in vote_1 and vote_1['candidate'] == 'Erick'
    assert 'result' in vote_1 and vote_1['result'] == 1

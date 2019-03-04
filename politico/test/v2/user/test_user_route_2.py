import pytest
from ...base import test_client, token, standard, error_standard

prefix = '/api/v2'


@pytest.fixture(scope='module')
def user():
    user = {
            "email": "erycoking360@gmail.com",
            "firstname": "erycoking",
            "id_no": "30761234",
            "lastname": "Lomunyak",
            "othername": "Loningo",
            "passport_url": "http://passports.com/passport167.png",
            "phone_number": "0700719300", 
            "username":"erycoking",
            "password":"erycoking"
        }
    return user


@pytest.fixture(scope='module')
def user_2():
    user = {
            "email": "erycoking360@gmail.com",
            "firstname": "clinton",
            "lastname": "Lomunyak",
            "id_no": "30303094",
            "othername": "Loningo",
            "passport_url": "http://passports.com/passport4.png",
            "phone_number": "0702554146", 
            "username":"erycoking",
            "password":"erycoking"
        }
    return user


@pytest.fixture(scope='module')
def bad_user():
    user = {
            "email": "@erycoking360gmail.com",
            "firstname": "erycoking",
            "id_no": "30761234",
            "othername": "Loningo",
            "passport_url": "http://passports.com/passport4.png",
            "phone_number": "0702554146", 
            "username":"erycoking",
            "password":"erycoking"
        }
    return user

@pytest.fixture(scope='module')
def bad_user_2():
    user = {
            "email": "erycoking360@gmail.com",
            "firstname": "erycoking",
            "id_no": "30761234",
            "lastname": "Lomunyak",
            "othername": "Loningo",
            "passport_url": "http://passports.com/passport4.png",
            "phone_number": "0702554146", 
            "password":"erycoking"
        }
    return user


def test_create_users(test_client, user):
    response = test_client.post(prefix + '/auth/signup', json = user)
    assert response.status_code == 200
    data = standard(response)
    user_data = data['data'][0]
    assert 'token' in user_data
    user = user_data['user']
    assert 'firstname' in user and user['firstname'] == 'erycoking'
    assert 'lastname' in user and user['lastname'] == 'Lomunyak'
    

def test_create_bad_user(test_client, bad_user):
    response = test_client.post(prefix + '/auth/signup', json = bad_user)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'lastname missing'

def test_create_bad_user_2(test_client, bad_user_2):
    response = test_client.post(prefix + '/auth/signup', json = bad_user_2)
    assert response.status_code == 400
    data = error_standard(response)
    message = data['error']
    assert message == 'username missing'

def test_login(test_client):
    login_credentials = dict(
        username='pheonix',
        password='admin123'
    )
    response = test_client.post(prefix + '/auth/login', json = login_credentials)
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'token' in data[0]
    user = data[0]['user']
    assert 'firstname' in user and user['firstname'] == 'Erick'
    assert 'lastname' in user and user['lastname'] == 'Lomunyak'

def test_get_all_users(test_client, token):
    url = prefix + '/users'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 2
    user_1 = data[1]
    assert user_1 is not None
    assert 'firstname' in user_1 and user_1['firstname'] == 'erycoking'
    assert 'lastname' in user_1 and user_1['lastname'] == 'Lomunyak'

def test_get_single_user(test_client, token):
    url = prefix + '/users/2'
    response = test_client.open(url, method='GET', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert len(data) == 1
    user_1 = data[0]
    assert user_1 is not None
    assert 'firstname' in user_1 and user_1['firstname'] == 'erycoking'
    assert 'lastname' in user_1 and user_1['lastname'] == 'Lomunyak'

def test_update_users(test_client, token, user_2):
    url = prefix + '/users/2'
    response = test_client.open(url, method='PATCH', headers={
            'Authorization': 'Bearer {}'.format(token)
        }, json=user_2
    )
    print(response.get_json())
    assert response.status_code == 200
    data = standard(response)
    user = data['data'][0]
    assert 'firstname' in user and user['firstname'] == 'clinton'
    assert 'lastname' in user and user['lastname'] == 'Lomunyak'

def test_delete_single_user(test_client, token):
    url = prefix + '/users/2'
    response = test_client.open(url, method='DELETE', headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    response_data = standard(response)
    data = response_data['data']
    assert 'message' in data[0]
    assert data[0]['message'] == 'user with id:2 deleted'
    






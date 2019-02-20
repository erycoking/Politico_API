import pytest
from ....base import test_client
# from ....base import BaseTest

prefix = '/api/v2'


@pytest.fixture(scope='module')
def user():
    user = {
            "email": "erycoking360@gmail.com",
            "firstname": "erycoking",
            "id_no": "30761234",
            "is_admin": True,
            "lastname": "Lomunyak",
            "othername": "Loningo",
            "passport_url": "http://passports.com/passport4.png",
            "phone_number": "0702554146", 
            "username":"erycoking",
            "password":"erycoking"
        }
    return user


def test_create_users(test_client, user):
    response = test_client.post(prefix + '/auth/signup', json = user)
    assert response.status_code == 200
    data = response.get_json()
    user = data['data'][0]
    assert 'token' in user
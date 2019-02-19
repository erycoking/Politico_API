from ....base import test_client


prefix = '/api/v2'
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


def create_user(test_client):
    return test_client.post(prefix + '/auth/signup', json = user, follow_redirects=True)

def test_create_users(test_client):
    response = create_user(test_client)
    # assert test_client.assert_called_with(prefix + '/auth/signup', json = user)
    print(response)
    assert response is not None
    user = response['data'][0]
    assert user['token'] is not None
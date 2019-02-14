import pytest
from politico.api.v2.db.db import DB
from politico.api.v2.users.model import UserTable


@pytest.fixture(scope='module')
def cursor():
    print('Initilizing database')
    db = DB()
    conn = db.connection(True)
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()
    print('Tearing Down database connection')

@pytest.fixture(scope='module')
def user_tb(cursor):
    table = UserTable()
    yield table

@pytest.fixture(scope='module')
def user_1():
    user_data = {
        "email": "eryco@gmail.com",
        "firstname": "king",
        "id_no": "12345608",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "",
        "passport_url": "file/passports/passport1.png",
        "phone_number": "0712345678", 
        "username":"baller",
        "password":"password"
    }
    return user_data

@pytest.fixture(scope='module')
def user_2():
    user_data = {
        "email": "erycoking@gmail.com",
        "firstname": "king",
        "id_no": "12345678",
        "is_admin": True,
        "lastname": "rozay",
        "othername": "",
        "passport_url": "file/passports/passport1.png",
        "phone_number": "0712345609", 
        "username":"rozay",
        "password":"password"
    }
    return user_data

def test_create_user(user_tb, user_1):
    user = user_tb.add_user(user_1)
    assert user.get('lastname') == 'rozay'
    assert user.get('phone_number') == '0712345678'

def test_get_one_user(user_tb):
    user = user_tb.get_single_user(1)
    assert user.get('firstname') == 'king'
    assert user.get('email') == 'eryco@gmail.com'

def test_get_all_users(user_tb):
    users = user_tb.get_all_users()
    assert len(users) == 1
    user = users[0]
    assert user.get('lastname') == 'rozay'
    assert user.get('phone_number') == '0712345678'

def test_get_user_with_email(user_tb):
    user = user_tb.get_user_with_email('eryco@gmail.com')
    assert user.get('lastname') == 'rozay'
    assert user.get('phone_number') == '0712345678'

def test_update_user(user_tb):
    user = user_tb.update_user(1, user_2)
    assert user.get('username') == 'rozay'
    assert user.get('email') == 'erycoking@gmail.com'

def test_delete_user(user_tb):
    user_deleted = user_tb.delete_user(1)
    assert user_deleted == True
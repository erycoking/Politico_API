"""tests for the user model class"""

# core imports
import pytest

# custom imports
from politico.api.v1.user.model import User
from politico.api.v1.user.model import UserTable

# global variable
user_table = None

# initalizing user_table 
def setup_module():
    """initializing"""
    global user_table
    user_table = UserTable()


# creating test date
@pytest.fixture(scope='module')
def user_data():
    """test data"""
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

# creating test data
@pytest.fixture(scope='module')
def user_data_2():
    """test data"""
    user_data = {
        "email": "erycoking@gmail.com",
        "firstname": "mike",
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

def test_add_user(user_data):
    """testing add_user method"""
    new_user_data = user_table.add_user(user_data)
    assert new_user_data['id'] == 1
    assert new_user_data['firstname'] == 'king'

def test_get_user_with_id(user_data):
    """testing get_user_with_id method"""
    retrived_user = user_table.users.get(1)
    assert retrived_user['lastname'] == 'rozay'

def test_get_user_with_email(user_data):
    """testing get_user_with_email method"""
    retrived_user = user_table.get_user_with_email(user_data['email'])
    assert retrived_user['lastname'] == 'rozay'

def test_update_user(user_data_2):
    """testing update_user method"""
    updated_user = user_table.update_user(1, user_data_2)
    assert updated_user['firstname'] == 'mike'
    assert updated_user['id'] == 1
    assert len(user_table.users) == 1

def test_get_all_users(user_data):
    """testing get_all_users method"""
    user_table.add_user(user_data)
    retrieved_users = user_table.users
    first_user = retrieved_users.get(1)
    print(retrieved_users)
    assert first_user['firstname'] == 'king'
    assert len(retrieved_users) == 1

def test_delete_user():
    """testing delete_user method"""
    deleted = user_table.delete_user(1)
    assert deleted == True

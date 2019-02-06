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

def test_add_user(user_data):
    """testing add_user method"""
    new_user_data = user_table.add_user(user_data)
    assert new_user_data['id'] == 1
    assert new_user_data['full_name'] == 'king rozay'

def test_get_user_with_id(user_data):
    """testing get_user_with_id method"""
    retrived_user = user_table.get_user_with_id(1)
    assert retrived_user.lastname == 'rozay'

def test_get_user_with_email(user_data):
    """testing get_user_with_email method"""
    retrived_user = user_table.get_user_with_email(user_data['email'])
    assert retrived_user.lastname == 'rozay'

def test_update_user(user_data):
    """testing update_user method"""
    updated_user = user_table.update_user(1, user_data)
    assert updated_user['full_name'] == 'king rozay'

def test_get_all_users(user_data):
    """testing get_all_users method"""
    retrieved_users = user_table.get_all_users()
    assert retrieved_users[0]['firstname'] == 'king'

def test_delete_user():
    """testing delete_user method"""
    deleted = user_table.delete_user(1)
    assert deleted == True

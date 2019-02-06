"""tests for the user model class"""

# core imports
import pytest

# custom imports
from politico.api.v1.party.model import Party
from politico.api.v1.party.model import PartyTable

# global variable
party_table = None

# initalizing party_table 
def setup_module():
    """initializing"""
    global party_table
    party_table = PartyTable()


# creating test date
@pytest.fixture(scope='module')
def party_data():
    """test data"""
    party_data = {
        "hq_address": "Westlands, Nairobi",
        "logo_url": "logo/logo.jpg",
        "name": "jubilee"
    }
    return party_data

def test_add_user(party_data):
    """testing add_party method"""
    new_party_data = party_table.add_party(party_data)
    assert new_party_data['id'] == 1
    assert new_party_data['name'] == 'jubilee'

def test_get_user_with_id(party_data):
    """testing get_single_party method"""
    retrived_party = party_table.get_single_party(1)
    assert retrived_party.name == 'jubilee'

def test_get_user_with_email(party_data):
    """testing get_single_party_by_name method"""
    retrived_party = party_table.get_single_party_by_name(party_data['name'])
    assert retrived_party.name == 'jubilee'

def test_update_user(party_data):
    """testing update_party method"""
    updated_user = party_table.update_party(1, party_data)
    assert updated_user['name'] == 'jubilee'

def test_get_all_users(party_data):
    """testing get_all_parties method"""
    retrieved_parties = party_table.get_all_parties()
    assert retrieved_parties[0]['name'] == 'jubilee'

def test_delete_user():
    """testing delete_party method"""
    deleted = party_table.delete_party(1)
    assert deleted == True

"""test cases for the office model"""
 
#  import core module
import pytest

# importing custom modules 
from politico.api.v1.office.model import Office
from politico.api.v1.office.model import OfficeTable

# global variable
office_table = None

def setup_module():
    # initializing
    global office_table
    office_table = OfficeTable()

@pytest.fixture(scope='module')
def office_data():
    """test data"""
    # federal, legislative, state, or local government -> types of office
    office_data = {
        "type": "state", 
        "name": "president"
    }
    return office_data

@pytest.fixture(scope='module')
def office_data_2():
    """test data for updating"""
    office_data_2 = {
        "type": "state", 
        "name": "member of paliament"
    }
    return office_data_2

def test_add_office(office_data):
    # tests adding user to the database
    added_office = office_table.add_office(office_data)
    assert added_office.get('id') == 1
    assert added_office.get('name') == 'president'
    assert added_office.get('type') in ['federal', 'legislative', 'state', 'local_government']
    assert added_office.get('type') == 'state'

def test_update_office(office_data_2):
    # test updating an office information
    updated_office = office_table.update_office(1, office_data_2)
    assert updated_office.get('id') == 1
    assert updated_office.get('type') in ['federal', 'legislative', 'state', 'local_government']
    assert updated_office.get('type') == 'state'
    assert updated_office.get('name') == 'member of paliament'

def test_get_all_offices():
    # test getting all offices
    offices = office_table.get_all_offices()
    assert offices is not None
    assert offices[0]['id'] == 1
    assert offices[0]['type'] in ['federal', 'legislative', 'state', 'local_government']
    assert offices[0]['name'] == 'member of paliament'
    assert offices[0]['type'] == 'state'

def test_get_single_office():
    # tests getting a single office
    retrieved_office = office_table.get_single_office(1)
    assert retrieved_office.id == 1
    assert retrieved_office.type in ['federal', 'legislative', 'state', 'local_government']
    assert retrieved_office.type == 'state'
    assert retrieved_office.name == 'member of paliament'

def test_delete_office():
    # tests deleting an office
    office_deleted = office_table.delete_office(1)
    assert office_deleted == True
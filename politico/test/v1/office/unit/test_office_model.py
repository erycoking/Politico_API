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
    offices = office_table.offices
    print(offices)
    first_office = offices.get(1)
    assert first_office is not None
    print(first_office)
    assert first_office['id'] == 1
    assert first_office['type'] in ['federal', 'legislative', 'state', 'local_government']
    assert first_office['name'] == 'member of paliament'
    assert first_office['type'] == 'state'

def test_get_single_office():
    # tests getting a single office
    retrieved_office = office_table.offices.get(1)
    assert retrieved_office.get('id') == 1
    assert retrieved_office.get('type') in ['federal', 'legislative', 'state', 'local_government']
    assert retrieved_office.get('type') == 'state'
    assert retrieved_office.get('name') == 'member of paliament'

def test_delete_office():
    # tests deleting an office
    office_deleted = office_table.delete_office(1)
    assert office_deleted == True
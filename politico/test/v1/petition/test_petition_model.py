import pytest

from politico.api.v1.petition.model import PetitionTable

petition_table = None

def setup_module():
    # initialization
    global petition_table
    petition_table = PetitionTable()

@pytest.fixture(scope='module')
def petition_data():
    petition_data = {}
    petition_data['created_by'] = 1
    petition_data['office'] = 1
    petition_data['body'] = 'election irregularites'
    return petition_data

@pytest.fixture(scope='module')
def petition_data_2():
    petition_data_2 = {}
    petition_data_2['created_by'] = 2
    petition_data_2['office'] = 2
    petition_data_2['body'] = 'election rigging'
    return petition_data_2

def test_create_petition(petition_data):
    created_petition = petition_table.add_petition(petition_data)
    assert created_petition['id'] ==  1
    assert created_petition['body'] ==  'election irregularites'


def test_update_petition(petition_data_2):
    updated_petition = petition_table.update_petition(1, petition_data_2)
    assert updated_petition['id'] ==  1
    assert updated_petition['body'] ==  'election rigging'

def test_get_single_petition():
    petition = petition_table.petitions.get(1)
    assert petition['id'] ==  1
    assert petition['body'] ==  'election rigging'

def test_get_all_petitions():
    all_petition = petition_table.petitions
    assert all_petition is not None
    assert len(all_petition) == 1

def test_delete_petition():
    del_petition = petition_table.delete_petition(1)
    assert del_petition == True


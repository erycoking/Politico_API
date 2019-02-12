import pytest

from politico.api.v1.candidate.model import CandidateTable

cand_table = None

def setup_module():
    global cand_table
    cand_table = CandidateTable()

@pytest.fixture(scope='module')
def cand_data():
    cand_data = {}
    cand_data['candidate'] = 1
    cand_data['office'] = 1
    cand_data['party'] = 1
    return cand_data

@pytest.fixture(scope='module')
def cand_data_2():
    cand_data_2 = {}
    cand_data_2['candidate'] = 2
    cand_data_2['office'] = 2
    cand_data_2['party'] = 2
    return cand_data_2

def test_add_candidate(cand_data):
    added_candidate = cand_table.add_candidate(cand_data)
    assert added_candidate['id'] == 1
    assert added_candidate['office']  == 1

def test_update_candidate(cand_data_2):
    updated_candidate = cand_table.update_candidate(1, cand_data_2)
    assert updated_candidate['id'] == 1
    assert updated_candidate['office']  == 2

def test_get_all_candidates():
    all_candidates = cand_table.candidates
    print(all_candidates)
    assert all_candidates is not None
    assert len(all_candidates) == 1

def test_get_single_candidate():
    cand = cand_table.candidates.get(1)
    assert cand['id'] == 1
    assert cand['office']  == 2

def test_delete_candidate():
    candidate_deleted = cand_table.delete_candidate(1)
    assert candidate_deleted == True
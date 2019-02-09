import pytest
from politico.api.v1.vote.model import VotesTable

vote_table = None

def setup_module():
    global vote_table
    vote_table = VotesTable()

@pytest.fixture(scope='module')
def vote():
    vote = {}
    vote['office'] = 1
    vote['candidate'] = 1
    vote['created_by']=1
    return vote


@pytest.fixture(scope='module')
def second_vote():
    second_vote = {}
    second_vote['office'] = 2
    second_vote['candidate'] = 2
    second_vote['created_by'] = 2
    return second_vote


def test_cast_vote(vote):
    casted_vote = vote_table.cast_vote(vote)
    assert casted_vote.get('id') == 1
    assert casted_vote.get('office') == vote.get('office')
    assert casted_vote.get('candidate') == vote.get('candidate')
    assert casted_vote.get('created_by') == vote.get('created_by')
    assert len(vote_table.get_all_votes()) == 1

def test_update_casted_vote(second_vote):
    updated_vote = vote_table.update_vote(1, second_vote)
    assert updated_vote.get('id') == 1
    assert updated_vote.get('office') == second_vote.get('office')
    assert updated_vote.get('candidate') == second_vote.get('candidate')
    assert updated_vote.get('created_by') == second_vote.get('created_by')
    assert len(vote_table.get_all_votes()) == 1

def test_get_all_votes(vote):
    vote_table.cast_vote(vote)
    all_votes = vote_table.get_all_votes()
    assert all_votes is not None
    assert len(all_votes) == 2
    assert all_votes[0]['office'] == 2
    assert all_votes[1]['office'] == 1

def test_get_single_vote():
    vote_cast = vote_table.get_single_vote(1)
    assert vote_cast.created_by == 2
    assert vote_cast.office == 2
   
def test_delete_vote():
    deleted_vote  = vote_table.delete_vote(1)
    assert deleted_vote == True
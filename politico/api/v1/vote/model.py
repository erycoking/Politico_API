"""A model for storing Votes"""

# datetime module import
import datetime

class Votes:
    """Vote model"""

    def __init__(self, id, created_by, office, candidate):
        self._id = id
        x = datetime.datetime.now()
        self._created_on = x.strftime("%x")
        self._created_by = created_by
        self._office = office
        self._candidate = candidate

    @property
    def id(self):
        # id getter
        return self._id

    @id.setter
    def id(self, id):
        # id setter
        self._id = id

    @property
    def created_on(self):
        # created_on getter
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        # created_on setter
        self._created_on = created_on

    @property
    def created_by(self):
        # created_by getter
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        # created_by setter
        self._created_by = created_by

    @property
    def office(self):
        # office getter
        return self._office

    @office.setter
    def office(self, office):
        # office getter
        self._office = office

    @property
    def candidate(self):
        # candidate getter
        return self._candidate

    @candidate.setter
    def candidate(self, candidate):
        # candidate setter
        self._candidate = candidate

    @property
    def vote_data(self):
        vote_data = {}
        vote_data['id'] = self._id
        vote_data['created_on'] = self._created_on
        vote_data['created_by'] = self._created_by
        vote_data['office'] = self._office
        vote_data['candidate'] = self._candidate
        return vote_data


class VotesTable:
    """Acts as a table for storing votes"""

    # list of all votes cast
    votes = []

    next_id = len(votes) + 1

    def get_all_votes(self):
        # returns all votes
        all_votes = []
        for v in self.votes:
            all_votes.append(v.vote_data)

        return all_votes

    def get_single_vote(self, id):
        # return a single vote using the specified id
        for v in self.votes:
            if v.id == int(id):
                return v

    def get_vote_by_created_by(self, voter):
        # returns a single vote using the specified voter id
        for v in self.votes:
            if v.created_by == int(voter):
                return v

    def cast_vote(self, vote_data):
        new_vote = Votes(
            self.next_id, 
            vote_data['created_by'], 
            vote_data['office'], 
            vote_data['candidate']
        )
        self.votes.append(new_vote)
        return new_vote.vote_data

    def update_vote(self, id, vote_data):
        # updates a vote
        for i in range(len(self.votes)):
            if self.votes[i].id == int(id):
                self.votes[i].created_by = vote_data['created_by']
                self.votes[i].office = vote_data['office']
                self.votes[i].candidate = vote_data['candidate']
                return self.votes[i].vote_data

    def delete_vote(self, id):
        # delete a vote
        for i in range(len(self.votes)):
            if self.votes[i].id == int(id):
                del self.votes[i]
                return True

        return False
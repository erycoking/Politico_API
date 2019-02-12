"""A model for storing candidates"""

class Candidate:
    """candidate model"""

    def __init__(self, id, office, party, candidate):
        self._id = id
        self._office = office
        self._party = party
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
    def office(self):
        # office getter
        return self._office

    @office.setter
    def office(self, office):
        # office getter
        self._office = office

    @property
    def party(self):
        # party getter
        return self._party

    @party.setter
    def party(self, party):
        # party setter
        self._party = party

    @property
    def candidate(self):
        # candidate getter
        return self._candidate

    @candidate.setter
    def candidate(self, cand):
        # candidate setter
        self._candidate = cand

    @property
    def candidate_data(self):
        candidate_data = {}
        candidate_data['id'] = self._id
        candidate_data['office'] = self._office
        candidate_data['party'] = self._party
        candidate_data['candidate'] = self._candidate
        return candidate_data


class CandidateTable:
    """Candidate Table"""

    candidates = {}
    next_id = len(candidates) + 1


    def get_candidate_by_candidate(self, cand_id):
        # return a single candidate with the specified candidate key
        for cand in self.candidates.values():
            if cand['candidate'] == int(cand_id):
                return cand

    def add_candidate(self, cand_data):
        # add a candidate to the candidate list
        new_candidate = Candidate(
            self.next_id, 
            cand_data['office'], 
            cand_data['party'], 
            cand_data['candidate']
        )
        self.candidates[self.next_id] = new_candidate.candidate_data
        return self.candidates[self.next_id]

    def update_candidate(self, id, cand_data):
        # updates candidate information 
        candidate = self.candidates.get(id)
        candidate['office'] = cand_data['office']
        candidate['party'] = cand_data['party']
        candidate['candidate'] = cand_data['candidate']
        self.candidates[id] = candidate
        return self.candidates.get(id)


    def delete_candidate(self, id):
        # deletes a candidate
        candidate = self.candidates.get(id)
        if candidate:
            del self.candidates[id]
            return True
        return False 

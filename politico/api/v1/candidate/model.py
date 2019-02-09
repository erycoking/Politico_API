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

    candidates = []
    next_id = len(candidates) + 1

    def get_all_candidates(self):
        # returns a list of all candidates
        all_candidates = []
        for cand in self.candidates:
            all_candidates.append(cand.candidate_data)

        return all_candidates

    def get_single_candidate(self, id):
        # return a single candidate with the specified id
        for cand in self.candidates:
            if cand.id == int(id):
                return cand

    def get_candidate_by_candidate(self, cand):
        # return a single candidate with the specified candidate key
        for cand in self.candidates:
            if cand.candidate == int(cand):
                return cand

    def add_candidate(self, cand_data):
        # add a candidate to the candidate list
        new_candidate = Candidate(
            self.next_id, 
            cand_data['office'], 
            cand_data['party'], 
            cand_data['candidate']
        )
        self.candidates.append(new_candidate)
        return new_candidate.candidate_data

    def update_candidate(self, id, cand_data):
        # updates candidate information 
        for i in range(len(self.candidates)):
            if self.candidates[i].id == int(id):
                self.candidates[i].office = cand_data['office']
                self.candidates[i].party = cand_data['party']
                self.candidates[i].candidate = cand_data['candidate']
                return self.candidates[i].candidate_data

    def delete_candidate(self, id):
        # deletes a candidate
        for i in range(len(self.candidates)):
            if self.candidates[i].id == int(id):
                del self.candidates[i]
                return True

        return False 

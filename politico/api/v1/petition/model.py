"""A model for storing Petition"""

# datetime module import
import datetime

class Petition:
    """Petition model"""

    def __init__(self, id, created_by, office, body):
        # constructor
        self._id = id
        x = datetime.datetime.now()
        self._created_on = x.strftime("%x")
        self._created_by = created_by
        self._office = office
        self._body = body

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
    def body(self):
        # body getter
        return self._body

    @body.setter
    def body(self, cand):
        # body setter
        self._body = cand

    @property
    def petition_data(self):
        # return petition data
        petition_data = {}
        petition_data['id'] = self._id
        petition_data['created_on'] = self._created_on
        petition_data['created_by'] = self._created_by
        petition_data['office'] = self._office
        petition_data['body'] = self._body
        return petition_data


class PetitionTable:
    """Acts as a table for storing petitions"""

    # list of petitions
    petitions = {}
    next_id = len(petitions) + 1

    def add_petition(self, petition_data):
        # adds a new petition
        new_petition = Petition(
            self.next_id, 
            petition_data['created_by'], 
            petition_data['office'], 
            petition_data['body']
        )
        self.petitions[self.next_id] = new_petition.petition_data
        return new_petition.petition_data

    def update_petition(self, id, petition_data):
        # updates petition data
        petition = self.petitions.get(id)
        petition['created_by'] = petition_data['created_by']
        petition['office'] = petition_data['office']
        petition['body'] = petition_data['body']
        self.petitions[id] = petition
        return self.petitions[id]

    def get_petition_by_created_by(self, creator):
        for p in self.petitions.values():
            if p['created_by'] == int(creator):
                return p


    def delete_petition(self, id):
        # deletes a petition
        petition = self.petitions.get(id)
        if petition:
            del self.petitions[id]
            return True 

        return False


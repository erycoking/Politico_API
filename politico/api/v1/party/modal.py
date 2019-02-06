"""
    contains the class for party modal
"""

class Party:
    def __init__(self, id, name, hqAddress, logoUrl):
        self.id = id
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, id):
        self.id = id

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def hqAddress(self):
        return self.hqAddress

    @hqAddress.setter
    def hqAddress(self, hqAddress):
        self.hqAddress = hqAddress

    @property
    def logoUrl(self):
        return self.logoUrl

    @logoUrl.setter
    def logoUrl(self, logoUrl):
        self.logoUrl = logoUrl


    @property
    def party_data(self):
        party_data = {}
        party_data['id'] = self.id
        party_data['name'] = self.name
        party_data['hqAddress'] = self.hqAddress
        party_data['logoUrl'] = self.logoUrl
        return party_data

    @property
    def party_patch(self):
        party_patch = {}
        party_patch['id'] = self.id
        party_patch['name'] = self.name
        return party_patch


class partyTable:
    """ acts as a table for storing parties and their related information"""

    def __init__(self):
        pass

    parties = [
        Party(1, 'ygb', 'Westlands, Nairobi', 'logo/logo.jpg')
    ]

    next_id = len(parties) + 1

    def get_all_parties(self):
        # returns all parties
        all_parties = []
        for party in self.parties:
            all_parties.append(party.party_data)
        return all_parties

    def get_single_party(self, id):
        # gets a single party by id
        for party in self.parties:
            if party.id == int(id):
                return party

    def get_single_party_by_name(self, name):
        # gets a single party by name
        for party in self.parties:
            if party.name == name:
                return party

    def add_party(self, party_data):
        # add a new party
        new_party = Party(
            self.next_id, 
            party_data['name'],
            party_data['hqAddress'], 
            party_data['logoUrl']
        )
        self.parties.append(new_party)
        return new_party.party_patch

    def update_party(self, id, party_data):
        # updates party data
        for i in range(len(self.parties)):
            if self.parties[i].id == id:
                self.parties[i].name = party_data['name']
                self.parties[i].hqAddress = party_data['hqAddress']
                self.parties[i].logoUrl = party_data['logoUrl']
                return self.parties[i].party_patch

    def delete_party(self, id):
        # deletes a party from the list of parties
        for i in range(len(self.parties)):
            if self.parties[i].id == id:
                del self.parties[i]
                return True

        return False

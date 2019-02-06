"""
    contains the class for party modal
"""

class Party:
    def __init__(self, id, name, hq_address, logo_url):
        self.id = id
        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url

    @property
    def id(self):
        return self.id

    @property
    def name(self):
        return self.name

    @property
    def hq_address(self):
        return self.hq_address

    @property
    def logo_url(self):
        return self.logo_url


    @property
    def party_data(self):
        party_data = {}
        party_data['id'] = self.id
        party_data['name'] = self.name
        party_data['hq_address'] = self.hq_address
        party_data['logo_url'] = self.logo_url
        return party_data

    @property
    def party_data_for_updates_and_deletes(self):
        party_data_for_updates_and_deletes = {}
        party_data_for_updates_and_deletes['id'] = self.id
        party_data_for_updates_and_deletes['name'] = self.name
        return party_data_for_updates_and_deletes


class PartyTable:
    """ acts as a table for storing parties and their related information"""

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
            party_data['hq_address'], 
            party_data['logo_url']
        )
        self.parties.append(new_party)
        return new_party.party_data_for_updates_and_deletes

    def update_party(self, id, party_data):
        # updates party data
        for i in range(len(self.parties)):
            if self.parties[i].id == id:
                self.parties[i].name = party_data['name']
                self.parties[i].hq_address = party_data['hq_address']
                self.parties[i].logo_url = party_data['logo_url']
                return self.parties[i].party_data_for_updates_and_deletes

    def delete_party(self, id):
        # deletes a party from the list of parties
        for i in range(len(self.parties)):
            if self.parties[i].id == id:
                del self.parties[i]
                return True

        return False

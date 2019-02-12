"""
    contains the class for party model
"""

class Party:
    def __init__(self, id, name, hq_address, logo_url):
        self._id = id
        self._name = name
        self._hq_address = hq_address
        self._logo_url = logo_url

    @property
    def id(self):
        # id getter
        return self._id

    @id.setter
    def id(self, id):
        # id setter
        return self._id

    @property
    def name(self):
        # name getter
        return self._name

    @name.setter
    def name(self, name):
        # name setter
        self._name = name

    @property
    def hq_address(self):
        # hq_address getter
        return self._hq_address

    @hq_address.setter
    def hq_address(self, address):
        # hq_address setter
        self._hq_address = address

    @property
    def logo_url(self):
        # logo getter
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo):
        # logo_url setter
        self._logo_url = logo


    @property
    def party_data(self):
        party_data = {}
        party_data['id'] = self._id
        party_data['name'] = self._name
        party_data['hq_address'] = self._hq_address
        party_data['logo_url'] = self._logo_url
        return party_data

    @property
    def party_data_for_updates_and_deletes(self):
        party_data_for_updates_and_deletes = {}
        party_data_for_updates_and_deletes['id'] = self._id
        party_data_for_updates_and_deletes['name'] = self._name
        return party_data_for_updates_and_deletes


class PartyTable:
    """ acts as a table for storing parties and their related information"""

    parties = {}
    next_id = len(parties) + 1
    prefix = 'party_'
    next_key = prefix + str(next_id)

    def get_all_parties(self):
        # returns all parties
        all_parties = []
        for party in self.parties.values():
            all_parties.append(party.party_data)
        return all_parties

    def get_single_party(self, id):
        # gets a single party by id
        key = self.prefix + str(id)
        return self.parties.get(key)

    def get_single_party_by_name(self, name):
        # gets a single party by name
        for party in self.parties.values():
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
        self.parties[self.next_key] = new_party
        return new_party.party_data_for_updates_and_deletes

    def update_party(self, id, party_data):
        # updates party data
        part_key = self.prefix + str(id)
        party = self.parties.get(part_key)
        party.name = party_data['name']
        party.hq_address = party_data['hq_address']
        party.logo_url = party_data['logo_url']
        self.parties[part_key] = party
        return party.party_data_for_updates_and_deletes

    def delete_party(self, id):
        # deletes a party from the list of parties
        party_key = self.prefix + str(id)
        party = self.parties.get(party_key)
        if party:
            del self.parties[party_key]
            return True
            
        return False

"""office model"""

class Office:
    """office data"""
    def __init__(self, id, type, name):
        # constructor
        self._id = id
        self._type = type
        self._name = name

    @property
    def id(self):
        # id getter
        return self._id

    @id.setter
    def id(self, id):
        # id setter
        self._id = id

    @property
    def type(self):
        # type getter
        return self._type

    @type.setter
    def type(self, type):
        # type setter
        self._type = type

    @property
    def name(self):
        # name getter
        return self._name

    @name.setter
    def name(self, name):
        # name setter
        self._name = name

    @property
    def office_data(self):
        # return office data
        office_data = {}
        office_data['id'] = self._id
        office_data['type'] = self._type
        office_data['name'] = self._name
        return office_data




class OfficeTable:
    """act as table for storing a list of tables"""

    offices = {}
    next_id = len(offices) + 1

    def get_office_by_name(self, name):
        # retrieve an office by name
        for ofc in self.offices.values():
            if ofc['name'] == name:
                return ofc

    def add_office(self, office_data):
        # add an office to the offices list
        new_office = Office(self.next_id, office_data['type'], office_data['name'])
        self.offices[self.next_id] = new_office.office_data
        return self.offices.get(self.next_id)

    def update_office(self, id, office_data):
        # updates an office
        office = self.offices.get(id)
        office['type'] = office_data['type']
        office['name'] = office_data['name']
        self.offices[id] = office
        return self.offices[id]

    def delete_office(self, id):
        # delete a single office
        office = self.offices.get(id)
        if office:
            del self.offices[id]
            return True
        return False
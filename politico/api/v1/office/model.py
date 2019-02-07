"""office model"""

class Office:
    """office data"""
    def __init__(self, id, type, name):
        # constructor
        self.id = id
        self.type = type
        self.name = name

    @property
    def id(self):
        # id getter
        return self.id

    @property
    def type(self):
        # type getter
        return self.type

    @property
    def name(self):
        # name getter
        return self.name

    @property
    def office_data(self):
        # return office data
        office_data = {}
        office_data['id'] = self.id
        office_data['type'] = self.type
        office_data['name'] = self.name
        return office_data



class OfficeTable:
    """act as table for storing a list of tables"""

    offices = []

    next_id = len(offices) + 1

    def get_all_offices(self):
        # returns all offices
        all_offices = []
        for ofc in self.offices:
            all_offices.append(ofc.office_data)
            
        return all_offices

    def get_single_office(self, id):
        # returns a single office
        for ofc in self.offices:
            if ofc.id == int(id):
                return ofc

    def add_office(self, office_data):
        # add an office to the offices list
        new_office = Office(self.next_id, office_data['type'], office_data['name'])
        self.offices.append(new_office)
        return new_office

    def update_office(self, id, office_data):
        # updates an office
        for i in range(len(self.offices)):
            if self.offices[i].id == int(id):
                self.offices[i].type = office_data['type']
                self.offices[i].name = office_data['name']
                return self.offices[i]

    def delete_office(self, id):
        # delete a single office
        for i in range(len(self.offices)):
            if self.offices[i].id == int(id):
                del self.offices[i]
                return True
        return False
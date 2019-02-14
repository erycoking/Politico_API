import psycopg2
from politico.api.v2.db.db import DB

class OfficeTable:
    """office table"""

    def __init__(self):
        self.db = DB()

    def get_one_office(self, id):
        office = self.db.fetch_one('office', 'id', id)
        if office is not None:
            return self.office_data(office)
        return None

    def get_one_office_by_name(self, name):
        office = self.db.fetch_one_using_string('office', 'name', name)
        if office is not None:
            return self.office_data(office)
        return None

    def get_offices(self):
        offices = []
        stored_offices = self.db.fetch_all('office')
        for office in stored_offices:
            offices.append(self.office_data(office))
        return offices

    def create_office(self, office_data):

        conn = self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into office(name, type) values(%s, %s) RETURNING id;""",  
                 (office_data.get('name'), office_data.get('type'))
                )
            office_data['id'] = cursor.fetchone()[0]
            cursor.commit()
            return office_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_office(self, id, office_data):
        conn =  self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update office set name = %s type = %s where id = %s RETURNING id;""", 
                (office_data.get('name'), office_data.get('type'))
            )
            office_data['id'] = cursor.fetchone()[0]
            cursor.commit()
            return office_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_office(self, id):
        return self.db.delete_one('office', 'id', id)

    def office_data(self, office):
        office_data = {}
        office_data['id'] = office[0]
        office_data['name'] = office[1]
        office_data['type'] = office[2]
        return office_data
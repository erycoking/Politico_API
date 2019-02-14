import psycopg2
from politico.api.v2.db.db import DB

class PartyTable:
    """class for manipulating party table"""

    def __init__(self):
        self.db = DB()

    def get_one_party(self, id):
        party = self.db.fetch_one('party', 'id', id)
        if party is not None:
            return self.party_data(party)
        return None

    def get_one_party_by_name(self, name):
        party = self.db.fetch_one_using_string('party', 'name', name)
        if party is not None:
            return self.party_data(party)
        return None

    def get_parties(self):
        parties = []
        stored_parties = self.db.fetch_all('party')
        for party in stored_parties:
            parties.append(self.party_data(party))
        return parties

    def create_party(self, party_data):

        conn = self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into party(name, hq_address, logo_url) values(%s, %s, %s);""",  
                 (party_data.get('name'), party_data.get('hq_address'), party_data('logo_url'))
                )
            party_added = {
                'id': cursor.fetchone()[0],
                'name': cursor.fetchone()[1]
            }
            cursor.commit()
            return party_added
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_party(self, id, party_data):
        conn =  self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update party set name = %s hq_address = %s logo_url = %s where id = %s;""", 
                (party_data.get('name'), party_data.get('hq_address'), party_data('logo_url', id))
            )
            update_party = {
                'id': cursor.fetchone()[0],
                'name': cursor.fetchone()[1]
            }
            cursor.commit()
            return update_party
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_party(self, id):
        return self.db.delete_one('party', 'id', id)

    def party_data(self, party):
        party_data = {}
        party_data['id'] = party[0]
        party_data['name'] = party[1]
        party_data['hq_address'] = party[2]
        party_data['logo_url'] = party[3]
        return party_data
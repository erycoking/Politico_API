import psycopg2
from politico.api.v2.db import DB

class PartyTable(DB):
    """class for manipulating party table"""

    def get_one_party(self, id):
        party = self.fetch_one('party', 'id', id)
        if party is not None:
            return self.party_data(party)
        return None

    def get_one_party_by_name(self, name):
        party = self.fetch_one_using_string('party', 'name', name)
        if party is not None:
            return self.party_data(party)
        return None

    def get_parties(self):
        parties = []
        stored_parties = self.fetch_all('party')
        for party in stored_parties:
            parties.append(self.party_data(party))
        return parties

    def create_party(self, party_data):

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into party(name, hq_address, logo_url) values(%s, %s, %s) RETURNING id;""", (
                    party_data['name'], party_data['hq_address'], party_data['logo_url']
                )
            )
            party_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return party_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_party(self, id, party_data):
        conn =  self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update party set name = %s, hq_address = %s, logo_url = %s where id = %s RETURNING id;""", 
                (party_data['name'], party_data['hq_address'], party_data['logo_url'], id)
            )
            party_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return party_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_party(self, id):
        return self.delete_one('party', 'id', id)

    def party_data(self, party):
        party_data = {}
        party_data['id'] = party[0]
        party_data['name'] = party[1]
        party_data['hq_address'] = party[2]
        party_data['logo_url'] = party[3]
        return party_data
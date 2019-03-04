import psycopg2
from politico.api.v2.db import DB
import datetime
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.users.model import UserTable

class PetitionTable(DB):
    """petition table"""

    def get_one_petition(self, id):
        petition = self.fetch_one('petition', 'id', id)
        if petition is not None:
            return self.petition_data(petition)
        return None

    def get_one_petition_by_created_by_and_office(self, created_by, office):
        petition = self.fetch_one_using_two_values('petition', 'created_by', created_by, 'office', office)
        if petition is not None:
            return self.petition_data(petition)
        return None

    def get_one_petition_by_created_by(self, created_by):
        petition = self.fetch_one('petition', 'created_by', created_by)
        if petition is not None:
            return self.petition_data(petition)
        return None

    def get_petitions(self):
        petitions = []
        stored_petitions = self.fetch_all('petition')
        for petition in stored_petitions:
            petitions.append(self.petition_data(petition))
        return petitions

    def create_petition(self, petition_data):
        office_tb = OfficeTable()
        office = office_tb.get_one_office_by_name(petition_data['office'])
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into petition(created_by, office, body, evidence) values(%s, %s, %s,  %s) RETURNING id;""",  
                 (petition_data['created_by'], office['id'], petition_data['body'], petition_data['evidence'])
                )
            conn.commit()
            petition_id = cursor.fetchone()[0]
            print(petition_id)
            petition_details = self.get_one_petition(petition_id)
            print(petition_details)
            return petition_details
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_petition(self, id, petition_data):
        office_tb = OfficeTable()
        office = office_tb.get_one_office_by_name(petition_data['office'])
        conn =  self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update petition set created_by = %s, office = %s, body = %s, evidence = %s where id = %s RETURNING id;""", 
                (petition_data['created_by'], office['id'], petition_data['body'], petition_data['evidence'], id)
            )
            conn.commit()
            petition_id = cursor.fetchone()[0]
            petition_details = self.get_one_petition(petition_id)
            return petition_details
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_petition(self, id):
        return self.delete_one('petition', 'id', id)

    def petition_data(self, petition):
        user_tb = UserTable()
        user = user_tb.get_single_user(petition[2])
        user_fullname = '' + user['firstname'] +' '+ user['lastname'] +' '+ user['othername']

        office_tb = OfficeTable()
        office = office_tb.get_one_office(petition[3])
        petition_data = {}
        petition_data['id'] = petition[0]
        petition_data['created_on'] = str(petition[1])
        petition_data['created_by'] = user_fullname
        petition_data['office'] = office['name']
        petition_data['body'] = petition[4]
        petition_data['evidence'] = petition[5]
        return petition_data
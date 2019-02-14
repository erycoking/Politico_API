import psycopg2
from politico.api.v2.db.db import DB

class PetitionTable:
    """petition table"""

    def __init__(self):
        self.db = DB()

    def get_one_petition(self, id):
        petition = self.db.fetch_one('petition', 'id', id)
        if petition is not None:
            return self.petition_data(petition)
        return None

    def get_one_petition_by_created_by(self, created_by):
        petition = self.db.fetch_one('petition', 'created_by', created_by)
        if petition is not None:
            return self.petition_data(petition)
        return None

    def get_petitions(self):
        petitions = []
        stored_petitions = self.db.fetch_all('petition')
        for petition in stored_petitions:
            petitions.append(self.petition_data(petition))
        return petitions

    def create_petition(self, petition_data):

        conn = self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into petition(created_by, office, body, evidence) values(%s, %s, %s,  %s) RETURNING id;""",  
                 (petition_data['created_by'], petition_data['office'], petition_data['body'], petition_data['evidence'])
                )
            petition_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return petition_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_petition(self, id, petition_data):
        conn =  self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update petition set created_by = %s, office = %s, body = %s, evidence = %s where id = %s RETURNING id;""", 
                (petition_data['created_by'], petition_data['office'], petition_data['body'], petition_data['evidence'], id)
            )

            petition_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return petition_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_petition(self, id):
        return self.db.delete_one('petition', 'id', id)

    def petition_data(self, petition):
        petition_data = {}
        petition_data['id'] = petition[0]
        petition_data['created_on'] = petition[1]
        petition_data['created_by'] = petition[2]
        petition_data['office'] = petition[3]
        petition_data['body'] = petition[4]
        petition_data['evidence'] = petition[5]
        return petition_data
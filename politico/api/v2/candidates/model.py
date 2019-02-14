import psycopg2
from politico.api.v2.db.db import DB

class CandidateTable:
    """candidates table"""

    def __init__(self):
        self.db = DB()

    def get_one_candidate(self, id):
        candidate = self.db.fetch_one('candidate', 'id', id)
        if candidate is not None:
            return self.candidate_data(candidate)
        return None

    def get_one_candidate_by_user(self, id):
        candidate = self.db.fetch_one('candidate', 'candidate', id)
        if candidate is not None:
            return self.candidate_data(candidate)
        return None

    def get_candidates(self):
        candidates = []
        stored_candidates = self.db.fetch_all('candidate')
        for candidate in stored_candidates:
            candidates.append(self.candidate_data(candidate))
        return candidates

    def create_candidate(self, candidate_data):

        conn = self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into candidates(office, party, candidate) values(%s, %s, %s) RETURNING id;""",  
                 (candidate_data.get('office'), candidate_data.get('party'), candidate_data('candidate'))
                )
            candidate_data['id'] = cursor.fetchone()[0]
            cursor.commit()
            return candidate_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_candidate(self, id, candidate_data):
        conn =  self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update candidates set office = %s party = %s candidate = %s where id = %s RETURNING id;""", 
                (candidate_data.get('office'), candidate_data.get('party'), candidate_data('candidate', id))
            )
            candidate_data['id'] = cursor.fetchone()[0]
            cursor.commit()
            return candidate_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_candidate(self, id):
        return self.db.delete_one('candidates', 'id', id)

    def candidate_data(self, candidate):
        candidate_data = {}
        candidate_data['id'] = candidate[0]
        candidate_data['office'] = candidate[1]
        candidate_data['party'] = candidate[2]
        candidate_data['candidate'] = candidate[3]
        return candidate_data
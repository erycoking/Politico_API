import psycopg2
from politico.api.v2.db import DB

class CandidateTable(DB):
    """candidates table"""
            
    def get_one_candidate(self, office_id, id):
        candidate = self.fetch_one_using_two_values('candidates','office', office_id, 'id', id)
        if candidate is not None:
            return self.candidate_data(candidate)
        return None

    def get_one_candidate_by_user(self, office_id, id):
        candidate = self.fetch_one_using_two_values('candidates','office', office_id, 'id', id)
        if candidate is not None:
            return self.candidate_data(candidate)
        return None

    def get_candidates(self, office_id):
        candidates = []
        stored_candidates = self.fetch_all_using_int_key('candidates', 'office', office_id)
        for candidate in stored_candidates:
            candidates.append(self.candidate_data(candidate))
        return candidates

    def create_candidate(self, office_id, candidate_data):

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into candidates(office, party, candidate) values(%s, %s, %s) RETURNING id;""",  
                 (office_id, candidate_data['party'], candidate_data['candidate'])
                )
            candidate_data['id'] = cursor.fetchone()[0]
            candidate_data['office'] = office_id
            conn.commit()
            return candidate_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_candidate(self, office_id, id, candidate_data):
        conn =  self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update candidates set office = %s, party = %s, candidate = %s where id = %s RETURNING id;""", 
                (office_id, candidate_data['party'], candidate_data['candidate'], id)
            )
            candidate_data['id'] = cursor.fetchone()[0]
            candidate_data['office'] = office_id
            conn.commit()
            return candidate_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_candidate(self, office_id, id):
        return self.delete_one('candidates', 'id', id)

    def candidate_data(self, candidate):
        candidate_data = {}
        candidate_data['id'] = candidate[0]
        candidate_data['office'] = candidate[1]
        candidate_data['party'] = candidate[2]
        candidate_data['candidate'] = candidate[3]
        return candidate_data
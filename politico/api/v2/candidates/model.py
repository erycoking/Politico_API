import psycopg2
from politico.api.v2.db import DB
from politico.api.v2.party.model import PartyTable
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.users.model import UserTable

class CandidateTable(DB):
    """candidates table"""
            
    def get_single_candidate(self, id):
        candidate = self.fetch_one('candidates', 'id', id)
        if candidate is not None:
            return self.candidate_data(candidate)
        return None

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
        party_tb = PartyTable()
        party_id = party_tb.get_one_party_by_name(candidate_data['party'])

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into candidates(office, party, candidate) values(%s, %s, %s) RETURNING id;""",  
                 (office_id, party_id['id'], candidate_data['candidate'])
                )
            conn.commit()
            cand_id = cursor.fetchone()[0]
            candidate_details = self.get_single_candidate(cand_id)
            return candidate_details
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_candidate(self, office_id, id, candidate_data):
        party_tb = PartyTable()
        party_id = party_tb.get_one_party_by_name(candidate_data['party'])
        conn =  self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update candidates set office = %s, party = %s, candidate = %s where id = %s RETURNING id;""", 
                (office_id, party_id['id'], candidate_data['candidate'], id)
            )
            conn.commit()
            cand_id = cursor.fetchone()[0]
            candidate_details = self.get_single_candidate(cand_id)
            return candidate_details
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
        user_tb = UserTable()
        user = user_tb.get_single_user(candidate[3])
        office_tb = OfficeTable()
        office = office_tb.get_one_office(candidate[1])
        party_tb = PartyTable()
        party = party_tb.get_one_party(candidate[2])
        candidate_data = {}
        candidate_data['id'] = candidate[0]
        candidate_data['office'] = office['name']
        candidate_data['party'] = party['name']
        candidate_data['candidate'] = user['fullname']
        candidate_data['candidate_photo_url'] = user['passport_url']
        return candidate_data
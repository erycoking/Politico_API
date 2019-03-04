import psycopg2
from politico.api.v2.db import DB
import datetime
from politico.api.v2.office.model import OfficeTable
from politico.api.v2.users.model import UserTable
from politico.api.v2.candidates.model import CandidateTable

class VotesTable(DB):
    """vote table"""

    def get_one_vote(self, id):
        vote = self.fetch_one('vote', 'id', id)
        if vote is not None:
            return self.vote_data(vote)
        return None

    def get_one_vote_created_by_and_office(self, created_by, office):
        vote = self.fetch_one_using_two_values('vote', 'created_by', created_by, 'office', office)
        if vote is not None:
            return self.vote_data(vote)
        return None

    def get_votes(self):
        votes = []
        stored_votes = self.fetch_all('vote')
        for vote in stored_votes:
            votes.append(self.vote_data(vote))
        return votes

    def create_vote(self, vote_data):
        office_tb = OfficeTable()
        office = office_tb.get_one_office_by_name(vote_data['office'])

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into vote(created_by, office, candidate) values(%s, %s, %s) RETURNING id;""",  
                 (vote_data['created_by'], office['id'], vote_data['candidate'])
                )
            conn.commit()
            vote_id = cursor.fetchone()[0]
            vote_details = self.get_one_vote(vote_id)
            return vote_details
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error': str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    # def update_vote(self, id, vote_data):
    #     office_tb = OfficeTable()
    #     office = office_tb.get_one_office_by_name(vote_data['office'])
    #     conn =  self.connection()
    #     try:
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             """update vote set created_by = %s, office = %s, candidate = %s where id = %s RETURNING id;""", 
    #             (vote_data['created_by'], office['office'], vote_data['candidate'], id)
    #         )
    #         conn.commit()
    #         vote_id = cursor.fetchone()[0]
    #         vote_details = self.get_one_vote(vote_id)
    #         return vote_details
    #     except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
    #         err = {'error': str(error)}
    #         print(err)
    #         return err
    #     finally:
    #         if conn is not None:
    #             conn.close()

    #     return None

    # def delete_vote(self, id):
    #     return self.delete_one('vote', 'id', id)

    def vote_data(self, vote):
        user_tb = UserTable()
        user = user_tb.get_single_user(vote[2])
        user_fullname = '' + user['firstname'] +' '+ user['lastname'] +' '+ user['othername']

        office_tb = OfficeTable()
        office = office_tb.get_one_office(vote[3])
        cand_tb = CandidateTable()
        cand = cand_tb.get_single_candidate(vote[4])
        vote_data = {}
        vote_data['id'] = vote[0]
        vote_data['created_on'] = str(vote[1])
        vote_data['created_by'] = user_fullname
        vote_data['office'] = office['name']
        vote_data['candidate'] = cand['candidate']
        return vote_data
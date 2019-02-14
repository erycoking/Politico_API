import psycopg2
from politico.api.v2.db.db import DB

class VotesTable:
    """vote table"""

    def __init__(self):
        self.db = DB()

    def get_one_vote(self, id):
        vote = self.db.fetch_one('vote', 'id', id)
        if vote is not None:
            return self.vote_data(vote)
        return None

    def get_one_vote_created_by(self, created_by):
        vote = self.db.fetch_one('vote', 'created_by', created_by)
        if vote is not None:
            return self.vote_data(vote)
        return None

    def get_votes(self):
        votes = []
        stored_votes = self.db.fetch_all('vote')
        for vote in stored_votes:
            votes.append(self.vote_data(vote))
        return votes

    def create_vote(self, vote_data):

        conn = self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into vote(created_by, office, candidate) values(%s, %s, %s) RETURNING id;""",  
                 (vote_data.get('created_by'), vote_data.get('office'), vote_data.get('candidate'))
                )
            vote_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return vote_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_vote(self, id, vote_data):
        conn =  self.db.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update vote set created_by = %s, office = %s, candidate = %s where id = %s RETURNING id;""", 
                (vote_data.get('created_by'), vote_data.get('office'), vote_data.get('candidate'), id)
            )
            vote_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return vote_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_vote(self, id):
        return self.db.delete_one('vote', 'id', id)

    def vote_data(self, vote):
        vote_data = {}
        vote_data['id'] = vote[0]
        vote_data['created_on'] = vote[1]
        vote_data['created_by'] = vote[2]
        vote_data['office'] = vote[3]
        vote_data['candidate'] = vote[4]
        return vote_data
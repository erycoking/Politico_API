import psycopg2
from politico.api.v2.db import DB

class OfficeTable(DB):
    """office table"""

    def get_one_office(self, id):
        office = self.fetch_one('office', 'id', id)
        if office is not None:
            return self.office_data(office)
        return None

    def get_one_office_by_name(self, name):
        office = self.fetch_one_using_string('office', 'name', name)
        if office:
            return self.office_data(office)
        return None

    def get_offices(self):
        offices = []
        stored_offices = self.fetch_all('office')
        for office in stored_offices:
            offices.append(self.office_data(office))
        return offices

    def create_office(self, office_data):

        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """insert into office(name, type) values(%s, %s) RETURNING id;""",  
                 (office_data['name'], office_data['type'])
                )
            office_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return office_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_office(self, id, office_data):
        conn =  self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """update office set name = %s, type = %s where id = %s RETURNING id;""", 
                (office_data['name'], office_data['type'], id)
            )
            office_data['id'] = cursor.fetchone()[0]
            conn.commit()
            return office_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error' : str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def delete_office(self, id):
        return self.delete_one('office', 'id', id)

    def office_data(self, office):
        office_data = {}
        office_data['id'] = office[0]
        office_data['name'] = office[1]
        office_data['type'] = office[2]
        return office_data


    def get_office_election_result(self, id):
        results = []
        # get office first
        # get all candidates in that office
        # get total votes for that votes candidate
        # return the results
        office = self.get_one_office(id)

        candidates = self.fetch_all_using_int_key('candidates', 'office', office['id'])
        for cand in candidates:
            print(cand)
            cand_detail = self.fetch_one('candidates', 'id', cand[0])
            user_details = self.fetch_one('users', 'id', cand_detail[3])
            print(user_details)
            fullname = ''
            if str(user_details[3]) != '':
                fullname = user_details[1] +' '+ user_details[3] +' '+ user_details[2]
            else:
                fullname = user_details[1] +' '+ user_details[2]
            votes = self.fetch_all_using_int_key('vote', 'candidate', cand[0])
            total_vote_for_specific_candidate = len(votes)

            candidate_result = {
                'office': office['name'], 
                'candidate': fullname, 
                'result': total_vote_for_specific_candidate
            }

            results.append(candidate_result)

        return results

import psycopg2
import os
from instance.config import APP_CONFIG

CONFIG_NAME = os.getenv('FLASK_ENV')
URL = APP_CONFIG[CONFIG_NAME].DATABASE_URL


class DB:
    """Database initialization class"""

    def tables(self):
        users = """
            create table if not exists users (
                id serial primary key not null, 
                firstname varchar(50) not null, 
                lastname varchar(50) not null, 
                othername varchar(50) not null, 
                email varchar(100) not null unique, 
                phone_number bigint not null unique, 
                passport_url varchar(255) not null unique, 
                id_no bigint not null unique, 
                is_admin bool not null, 
                username varchar(50) not null unique, 
                password varchar(255) not null
            );
        """
        
        party = """
            create table if not exists party(
                id serial primary key not null, 
                name varchar(100) not null unique, 
                hq_address varchar(255) not null, 
                logo_url varchar(255) not null unique
            );
        """

        office = """
            create table if not exists office(
                id serial primary key not null, 
                name varchar(50) not null unique, 
                type varchar(50) not null 
            );
        """

        candidates = """
            create table if not exists candidates(
                id serial not null unique, 
                office integer references office(id), 
                party integer references party(id), 
                candidate integer references users(id),
                primary key (office, candidate) 
            );
        """

        vote = """
            create table if not exists vote(
                id serial not null unique, 
                created_on date not null default current_date , 
                created_by integer references users(id), 
                office integer references office(id), 
                candidate integer references candidates(id), 
                primary key (office, created_by)
            );
        """

        petition = """
            create table if not exists petition(
                id serial primary key not null, 
                created_on date not null default current_date , 
                created_by integer references users(id), 
                office integer references office(id), 
                body text not null, 
                evidence text [] 
            );
        """
        queries = [users, party, office, candidates, vote, petition]
        return queries

    def connection(self):
        try:
            conn = psycopg2.connect(URL)
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def initialize_db(self):
        conn = self.connection()
        print('Intitializing ...')
        try:
            cursor = conn.cursor()

            queies = self.tables()
            for query in queies:
                cursor.execute(query)

            conn.commit()

            print('Database Inititialised')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def fetch_one(self, tb_name, search_key, value):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = %s" % (tb_name, search_key, value))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def fetch_one_using_two_values(self, tb_name, search_key, value, search_key_2, value_2):
        # value and value_2 are both integers
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = %s and %s = %s" % (tb_name, search_key, value, search_key_2, value_2))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def fetch_one_using_string(self, tb_name, search_key, value):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = '%s'" % (tb_name, search_key, value))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def fetch_one_using_strings_with_two_values(self, tb_name, search_key, value, search_key_2, value_2):
        # value and value_2 are both strings
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = '%s' and %s = '%s'" % (tb_name, search_key, value, search_key_2, value_2))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None


    def fetch_one_using_strings_as_first_values(self, tb_name, search_key, value, search_key_2, value_2):
        # value 1 str value 2 int
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = '%s' and %s = %s" % (tb_name, search_key, value, search_key_2, value_2))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None

    def fetch_one_using_strings_as_second_values(self, tb_name, search_key, value, search_key_2, value_2):
        # value 1 int value 2 str
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = %s and %s = %s" % (tb_name, search_key, value, search_key_2, value_2))
            result = cursor.fetchone()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()

        return None


    def fetch_all(self, tb_name):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s" % tb_name)
            result = cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()
        
        return None

    def fetch_all_using_int_key(self, tb_name, search_key, value):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = %s" % (tb_name, search_key, value))
            result = cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()
        
        return None

    def fetch_all_using_str_key(self, tb_name, search_key, value):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("select * from %s where %s = '%s'" % (tb_name, search_key, value))
            result = cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if conn is not None:
                conn.close()
        
        return None

    def delete_one(self, tb_name, search_key, value):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("delete from %s where %s = %s" % (tb_name, search_key, value))
            conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        finally:
            if conn is not None:
                conn.close()

        return False

    def delete_all(self, tb_name):
        conn = self.connection()
        try:
            cursor = conn.cursor()
            cursor.execute("delete from %s" % tb_name)
            conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        finally:
            if conn is not None:
                conn.close()

        return False


    def tables_to_delete(self):

        users = 'Drop table if exists users'
        party = 'Drop table if exists party'
        office = 'Drop table if exists office'
        candidates = 'Drop table if exists candidates'
        vote = 'Drop table if exists vote'
        petition = 'Drop table if exists petition'

        queries = [petition, vote, candidates, office, party, users]
        return queries

    def tear_down_test_database(self):
        conn = self.connection()
        print('Intitializing tear down...')
        try:
            cursor = conn.cursor()

            queies = self.tables_to_delete()
            for query in queies:
                cursor.execute(query)

            conn.commit()
            print('Database pulled down successfully')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        

    

import psycopg2

class DB:
    """Database initialization class"""

    def __init__(self):
        self._db_name = 'politico'
        self._test_db_name = 'test_politico'
        self._password = ''
        self._host = '127.0.0.1'
        self._port = 5432
        self._user = 'erycoking'
        self._conn = None

    def tables(self):
        users = """
            create table if not exists users (
                id serial primary key not null, 
                firstname varchar(20) not null, 
                lastname varchar(20) not null, 
                othername varchar(20) not null, 
                email varchar(50) not null unique, 
                phone_number integer not null unique, 
                passport_url varchar(255) not null, 
                id_no integer not null unique, 
                is_admin bool not null, 
                username varchar(20) not null unique, 
                password varchar(255) not null
            );
        """
        
        party = """
            create table if not exists party(
                id serial primary key not null, 
                name varchar(100) not null, 
                hq_address varchar(255) not null, 
                logo_url varchar(255) not null
            );
        """

        office = """
            create table if not exists office(
                id serial primary key not null, 
                name varchar(50) not null, 
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

    def connection(self, testing=False):
        try:
            connection_string = None
            if testing:
                connection_string = 'host={} port={} dbname={} user={} password={}'.format(
                    self._host, self._port, self._test_db_name, self._user, self._password
                )
            else:
                connection_string = 'host={} port={} dbname={} user={} password={}'.format(
                    self._host, self._port, self._db_name, self._user, self._password
                )
            
            self._conn = psycopg2.connect(connection_string)
            return self._conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def initialize_db(self):
        conn = self.connection()
        conn_2 = self.connection(True)
        print('Intitializing ...')
        try:
            cursor = conn.cursor()
            cursor_2 = conn_2.cursor()

            queies = self.tables()
            for query in queies:
                cursor.execute(query)
                cursor_2.execute(query)

            conn.commit()
            conn_2.commit()

            print('Database Inititialised')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()
        
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
            if self._conn is not None:
                self._conn.close()
        
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
            if self._conn is not None:
                self._conn.close()
        
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
            if self._conn is not None:
                self._conn.close()

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
            if self._conn is not None:
                self._conn.close()

        return False
        

    

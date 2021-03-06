import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from politico.api.v2.db import DB


"""Interact with the user table in the database """
class UserTable(DB):
    """class for user table interaction"""

    def get_single_user(self, id):
        user = self.fetch_one('users', 'id', id)
        if user is not None:
            return self.user_data_2(user)
        return None

    def get_all_users(self):
        all_users = []
        users = self.fetch_all('users')
        for user in users:
            all_users.append(self.user_data_2(user))
        return all_users

    def get_user_with_email(self, email):
        user = self.fetch_one_using_string('users', 'email', email)
        if user is not None:
            return self.user_data_2(user)
        return None

    def get_user_with_username(self, name):
        user = self.fetch_one_using_string('users', 'username', name)
        if user is not None:
            return self.user_data(user)
        return None
        
    def get_user_with_string(self, search_key, value):
        user = self.fetch_one_using_string('users', search_key, value)
        if user is not None:
            return self.user_data_2(user)
        return None

    def get_user_with_int(self, search_key, value):
        user = self.fetch_one('users', search_key, int(value))
        if user is not None:
            return self.user_data_2(user)
        return None


    def add_user(self, user_data):
        # add a new user to the users table
        
        conn =  self.connection()
        phone_no = str(user_data['phone_number'])
        phone = None
        if '+' in phone_no:
            phone = phone_no[1:]
        else:
            phone = phone_no

        if 'othername' not in user_data:
            user_data['othername'] = ''

        try:
            cursor = conn.cursor()
            password = generate_password_hash(user_data['password'], method='sha256')
            cursor.execute( 
                """insert into users(firstname, lastname, othername, email, phone_number, 
                passport_url, id_no, is_admin, username, password) values(%s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s) RETURNING id;""", (
                    user_data['firstname'], user_data['lastname'], user_data['othername'], 
                    user_data['email'], int(phone), user_data['passport_url'], 
                     int(user_data['id_no']), bool(0), user_data['username'], 
                    password
                )
            )
            conn.commit()
            user_id = cursor.fetchone()[0]
            user_data = self.get_single_user(user_id)
            return user_data
        except (Exception, psycopg2.DatabaseError, psycopg2.IntegrityError) as error:
            err = {'error': str(error)}
            print(err)
            return err
        finally:
            if conn is not None:
                conn.close()

        return None

    def update_user(self, id, user_data):
        # add a new user to the users list

        if 'othername' not in user_data:
            user_data['othername'] = ''

        conn = self.connection()
        try:
            cursor = conn.cursor()
            password = generate_password_hash(user_data['password'], method='sha256')
            cursor.execute(
                """update users set firstname = %s, lastname = %s, othername= %s, email = %s, 
                phone_number = %s, passport_url = %s, id_no = %s, is_admin = %s, username = %s, 
                password = %s where id = %s RETURNING id;""", (
                    user_data['firstname'], user_data['lastname'], user_data['othername'], 
                    user_data['email'], int(user_data['phone_number']), user_data['passport_url'], 
                    int(user_data['id_no']), bool(0), user_data['username'], 
                    password, id
                )
            )
            conn.commit()
            user_id = cursor.fetchone()[0]
            print(user_id)
            user_details = self.get_single_user(user_id)
            return user_details      
        except (Exception, psycopg2.DatabaseError) as error:
            err = {'error': str(error)}
            print(err)
            return err

        return None

    def update_user_password(self, id, user_data):
        # add a new user to the users list

        conn = self.connection()
        try:
            cursor = conn.cursor()
            password = generate_password_hash(user_data['password'], method='sha256')
            cursor.execute(
                """update users set password = %s where id = %s RETURNING id;""", (password, id)
            )
            conn.commit()
            user_id = cursor.fetchone()[0]
            print(user_id)
            user_details = self.get_single_user(user_id)
            return user_details      
        except (Exception, psycopg2.DatabaseError) as error:
            err = {'error': str(error)}
            print(err)
            return err

        return None

    def delete_user(self, id):
        return self.delete_one('users', 'id', id)

    def user_data(self, user):
        """gets user data"""
        user_data = {}
        user_data['id'] = user[0]
        user_data['firstname'] = user[1]
        user_data['lastname'] = user[2]
        user_data['othername'] = user[3]
        user_data['email'] = user[4]
        user_data['phone_number'] = user[5]
        user_data['passport_url'] = user[6]
        user_data['id_no'] = user[7]
        user_data['is_admin'] = user[8]
        user_data['username'] = user[9]
        user_data['password'] = user[10]
        if str(user[3]) != '':
            user_data['fullname'] = user[1] +' '+ user[3] +' '+ user[2]
        else:
            user_data['fullname'] = user[1] +' '+ user[2]
        return user_data

    def user_data_2(self, user):
        """gets user data"""
        user_data = {}
        user_data['id'] = user[0]
        user_data['firstname'] = user[1]
        user_data['lastname'] = user[2]
        user_data['othername'] = user[3]
        user_data['email'] = user[4]
        user_data['phone_number'] = user[5]
        user_data['passport_url'] = user[6]
        user_data['id_no'] = user[7]
        user_data['is_admin'] = user[8]
        if str(user[3]) != '':
            user_data['fullname'] = user[1] +' '+ user[3] +' '+ user[2]
        else:
            user_data['fullname'] = user[1] +' '+ user[2]
        return user_data


    

        
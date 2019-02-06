import bcrypt

"""
    A class to represent the student
"""
class User:
    """User class"""

    def __init__(self, id, firstname, lastname, othername, email, phone_number, passport_url, is_admin, id_no, username, password):
        """Constructor"""
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        self.is_admin = is_admin
        self.id_no = id_no
        self.username = username
        self.password = bcrypt.hashpw(password.encode('base64'), bcrypt.gensalt())


    @property
    def id(self):
        """id getter"""
        return self.id

    @property
    def firstname(self):
        """firstname getter"""
        return self.firstname

    @property
    def lastname(self):
        """lastname getter"""
        return self.lastname


    @property
    def othername(self):
        """othername getter"""
        return self.othername

    @property
    def email(self):
        """email getter"""
        return self.email

    @property
    def phone_number(self):
        """phone_number getter"""
        return self.phone_number


    @property
    def passport_url(self):
        """passport_url getter"""
        return self.passport_url

    @property
    def is_admin(self):
        """is_admin getter"""
        return self.is_admin

    @property
    def id_no(self):
        """id_no getter"""
        return self.id_no

    @property
    def username(self):
        """username getter"""
        return self.username

    @property
    def password(self):
        """password getter"""
        return self.password

    @property
    def full_name(self):
        """full_name getter"""
        return '{} {} {}'.format(self.firstname, self.othername, self.lastname)

    @full_name.setter
    def full_name(self, full_name):
        """full_name setter"""
        self.firstname, self.othername, self.lastname = full_name.split(' ')

    @property
    def user_data(self):
        """gets user data"""
        user_data = {}
        user_data['id'] = self.id
        user_data['firstname'] = self.firstname
        user_data['lastname'] = self.lastname
        user_data['othername'] = self.othername
        user_data['email'] = self.email
        user_data['phone_number'] = self.phone_number
        user_data['passport_url'] = self.passport_url
        user_data['is_admin'] = self.is_admin
        user_data['id_no'] = self.id_no
        user_data['username'] = self.username
        user_data['password'] = self.password
        return user_data

    @property
    def user_data_2(self):
        user_data_2 = {}
        user_data_2['id'] = self.id
        user_data_2['full_name'] = self.full_name
        return user_data_2


"""Acts as a table for storing users """
class UserTable:
    """User table class"""

    def __init__(self):
        pass

    # stores a list of users
    users = []

    next_id = len(users) + 1

    def get_all_users(self):
        all_users = []
        for person in self.users:
            all_users.append(person.user_data)

        return all_users



    def get_user_with_id(self, id):
        #  gets a single user that matches the user id
        for person in self.users:
            if person.id == int(id):
                return person

    def get_user_with_email(self, email):
        #  gets a single user that matches the user id
        for person in self.users:
            if person.email == str(email):
                return person


    def add_user(self, user_data):
        # add a new user to the users list
        new_user = User(
            self.next_id, 
            user_data['firstname'], 
            user_data['lastname'], 
            user_data['othername'], 
            user_data['email'], 
            user_data['phone_number'], 
            user_data['passport_url'], 
            user_data['is_admin'], 
            user_data['id_no'], 
            user_data['username'], 
            user_data['password']
        )
        self.users.append(new_user)
        return new_user.user_data_2

    def update_user(self, id, user_data):
        # add a new user to the users list

        for i in range(len(self.users)):
            if self.users[i].id == int(id):
                self.users[i].firstname = user_data['firstname']
                self.users[i].lastname = user_data['lastname']
                self.users[i].othername = user_data['othername']
                self.users[i].email = user_data['email']
                self.users[i].phone_number = user_data['phone_number']
                self.users[i].passport_url = user_data['passport_url']
                self.users[i].is_admin = user_data['is_admin']
                self.users[i].id_no = user_data['id_no']
                self.users[i].username = user_data['username']
                self.users[i].password = bcrypt.hashpw(user_data['password'].encode('base64'), bcrypt.gensalt())
                return self.users[i].user_data_2

        

    def delete_user(self, id):
        # deletes user in the user list
        for i in range(len(self.users)):
            if self.users[i].id == int(id):
                del self.users[i]
                return True
        
        return False

    

        
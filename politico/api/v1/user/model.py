import bcrypt

"""
    A class to represent the student
"""
class User:
    """User class"""

    def __init__(self, id, firstname, lastname, othername, email, phone_number, passport_url, is_admin, id_no, username, password):
        """Constructor"""
        self._id = id
        self._firstname = firstname
        self._lastname = lastname
        self._othername = othername
        self._email = email
        self._phone_number = phone_number
        self._passport_url = passport_url
        self._is_admin = is_admin
        self._id_no = id_no
        self._username = username
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


    @property
    def id(self):
        """id getter"""
        return self._id

    @id.setter
    def id(self, id):
        # id setter
        self._id = id

    @property
    def firstname(self):
        """firstname getter"""
        return self._firstname

    @firstname.setter
    def firstname(self, fname):
        # firstname setter
        self._firstname = fname

    @property
    def lastname(self):
        """lastname getter"""
        return self._lastname

    @lastname.setter
    def lastname(self, lname):
        # lastname setter
        self._lastname = lname


    @property
    def othername(self):
        """othername getter"""
        return self._othername

    @othername.setter
    def othername(self, oname):
        # othername setter
        self._othername = oname

    @property
    def email(self):
        """email getter"""
        return self._email

    @email.setter
    def email(self, email):
        # email setter
        self._email = email

    @property
    def phone_number(self):
        """phone_number getter"""
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone):
        # phone_number setter
        self._phone_number = phone


    @property
    def passport_url(self):
        """passport_url getter"""
        return self._passport_url

    @passport_url.setter
    def passport_url(self, passport):
        # passport_url setter
        self._passport_url = passport

    @property
    def is_admin(self):
        """is_admin getter"""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, admin):
        # is_admin setter
        self._is_admin = admin

    @property
    def id_no(self):
        """id_no getter"""
        return self._id_no

    @id_no.setter
    def id_no(self, id):
        # id_no setter
        self._id_no = id

    @property
    def username(self):
        """username getter"""
        return self._username

    @username.setter
    def username(self, name):
        # username setter
        self._username = name

    @property
    def password(self):
        """password getter"""
        return self._password

    @password.setter
    def password(self, passwd):
        # password setter
        self._password = passwd

    @property
    def full_name(self):
        """full_name getter"""
        if self._othername == "":
            return '{} {}'.format(self._firstname, self._lastname)
        return '{} {} {}'.format(self._firstname, self._othername, self._lastname)

    @property
    def user_data(self):
        """gets user data"""
        user_data = {}
        user_data['id'] = self._id
        user_data['firstname'] = self._firstname
        user_data['lastname'] = self._lastname
        user_data['othername'] = self._othername
        user_data['email'] = self._email
        user_data['phone_number'] = self._phone_number
        user_data['passport_url'] = self._passport_url
        user_data['is_admin'] = self._is_admin
        user_data['id_no'] = self._id_no
        return user_data

"""Acts as a table for storing users """
class UserTable:
    """User table class"""

    # stores a list of users
    users = {}
    next_id = len(users) + 1


    def get_user_with_email(self, email):
        #  gets a single user that matches the user id
        for person in self.users.values():
            if person['email'] == str(email):
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
        self.users[self.next_id] = new_user.user_data
        return self.users[self.next_id]

    def update_user(self, id, user_data):
        # add a new user to the users list
        user = self.users.get(id)
        user['firstname'] = user_data['firstname']
        user['lastname'] = user_data['lastname']
        user['othername'] = user_data['othername']
        user['email'] = user_data['email']
        user['phone_number'] = user_data['phone_number']
        user['passport_url'] = user_data['passport_url']
        user['is_admin'] = user_data['is_admin']
        user['id_no'] = user_data['id_no']
        user['username'] = user_data['username']
        user['password'] = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
        self.users[id] = user
        return self.users[id]

        

    def delete_user(self, id):
        # deletes user in the user list
        user = self.users.get(id)
        if user:
            del self.users[id]
            return True
        
        return False

    

        
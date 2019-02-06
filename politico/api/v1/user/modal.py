import bcrypt

"""
    A class to represent the student
"""
class User:
    """User class"""

    def __init__(self, id, firstname, lastname, othername, email, phoneNumber, passportUrl, isAdmin, idNo, username, password):
        """Constructor"""
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.email = email
        self.phoneNumber = phoneNumber
        self.passportUrl = passportUrl
        self.isAdmin = isAdmin
        self.idNo = idNo
        self.username = username
        self.password = bcrypt.hashpw(password.encode('base64'), bcrypt.gensalt())


    @property
    def id(self):
        """id getter"""
        return self.id

    @id.setter
    def id(self, id):
        """id setter"""
        self.id = id

    @property
    def firstname(self):
        """firstname getter"""
        return self.firstname

    @firstname.setter
    def firstname(self, fname):
        """firstname setter"""
        self.firstname = fname

    @property
    def lastname(self):
        """lastname getter"""
        return self.lastname

    @lastname.setter
    def lastname(self, lname):
        """lastname setter"""
        self.lastname = lname

    @property
    def othername(self):
        """othername getter"""
        return self.othername

    @othername.setter
    def othername(self, oname):
        """othername setter"""
        self.othername = oname

    @property
    def email(self):
        """email getter"""
        return self.email

    @email.setter
    def email(self, email):
        """email setter"""
        self.email = email

    @property
    def phoneNumber(self):
        """phoneNumber getter"""
        return self.phoneNumber

    @phoneNumber.setter
    def phoneNumber(self, pnumber):
        """phoneNumber setter"""
        self.phoneNumber = pnumber

    @property
    def passportUrl(self):
        """passportUrl getter"""
        return self.passportUrl

    @passportUrl.setter
    def passportUrl(self, url):
        """passportUrl setter"""
        self.passportUrl = url

    @property
    def isAdmin(self):
        """isAdmin getter"""
        return self.isAdmin

    @isAdmin.setter
    def isAdmin(self, admin):
        """isAdmin setter"""
        self.isAdmin = admin

    @property
    def idNo(self):
        """idNo getter"""
        return self.idNo

    @idNo.setter
    def idNo(self, no):
        """idNo setter"""
        self.idNo = no

    @property
    def username(self):
        """username getter"""
        return self.username

    @username.setter
    def username(self, uname):
        """username setter"""
        self.username = uname

    @property
    def password(self):
        """password getter"""
        return self.password

    @password.setter
    def password(self, pswd):
        """password setter"""
        self.password = pswd

    @property
    def fullName(self):
        """fullname getter"""
        return '{} {} {}'.format(self.firstname, self.othername, self.lastname)

    @fullName.setter
    def fullName(self, fullname):
        """fullname setter"""
        self.firstname, self.othername, self.lastname = fullname.split(' ')

    @property
    def user_data(self):
        """gets user data"""
        user_data = {}
        user_data['id'] = self.id
        user_data['firstname'] = self.firstname
        user_data['lastname'] = self.lastname
        user_data['othername'] = self.othername
        user_data['email'] = self.email
        user_data['phoneNumber'] = self.phoneNumber
        user_data['passportUrl'] = self.passportUrl
        user_data['isAdmin'] = self.isAdmin
        user_data['idNo'] = self.idNo
        user_data['username'] = self.username
        user_data['password'] = self.password
        return user_data

    @property
    def user_patch(self):
        user_patch = {}
        user_patch['id'] = self.id
        user_patch['fullname'] = self.fullName
        return user_patch


"""Acts as a table for storing users """
class userTable:
    """User table class"""

    def __init__(self):
        pass

    # stores a list of users
    users = [
        User(1,'Erick', 'Lomunyak', 'Loningo', 'erycoking360@gmail.com', '0712345678', 'file/passports/passport1.png', True, 123456789, 'erycoking', 'password')
    ]

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
            user_data['phoneNumber'], 
            user_data['passportUrl'], 
            user_data['isAdmin'], 
            user_data['idNo'], 
            user_data['username'], 
            user_data['password']
        )
        self.users.append(new_user)
        return new_user.user_patch

    def update_user(self, id, user_data):
        # add a new user to the users list

        for i in range(len(self.users)):
            if self.users[i].id == int(id):
                print('match found')
                self.users[i].firstname = user_data['firstname']
                self.users[i].lastname = user_data['lastname']
                self.users[i].othername = user_data['othername']
                self.users[i].email = user_data['email']
                self.users[i].phoneNumber = user_data['phoneNumber']
                self.users[i].passportUrl = user_data['passportUrl']
                self.users[i].isAdmin = user_data['isAdmin']
                self.users[i].idNo = user_data['idNo']
                self.users[i].username = user_data['username']
                self.users[i].password = bcrypt.hashpw(user_data['password'].encode('base64'), bcrypt.gensalt())
                return self.users[i].user_patch

        

    def delete_user(self, id):
        # deletes user in the user list
        for i in range(len(self.users)):
            if self.users[i].id == int(id):
                del self.users[i]
                return True
        
        return False

    

        
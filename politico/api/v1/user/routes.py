from flask import Blueprint, make_response, request, jsonify
from politico.api.v1.user.modal import userTable

user = Blueprint('user', __name__)

user_table = userTable()

@user.route('/users', methods=['GET'])
def get_user():
    return make_response(jsonify({
        'status': 200, 
        'data': user_table.get_all_users()
    }), 200)

@user.route('/users/<id>', methods=['GET'])
def get_single_user(id):    
    user = user_table.get_user_with_id(id)
    if user != None:
        return make_response(jsonify({
            'status': 200, 
            'data': [user]
        }), 200)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }))

@user.route('/users', methods=['POST'])
def addUser():
    user_data = request.get_json()
    msg = validateKeysInUser(user_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg
        }), 406)

    msg1 = validateValueInUser(user_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg1
        }), 406)

    msg2 = validateUserInputType(user_data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg2
        }), 406)

    user1 = user_table.get_user_with_email(user_data['email'])
    if not user1:
        added_user = user_table.add_user(user_data)
        return make_response(jsonify({
            'status': 201,
            'data': [added_user]
        }), 201)
    else:
        return make_response(jsonify({
            'status': 406,
            'error': 'user with email::{} already exists!!!'.format(user_data['email'])
        }), 406)


@user.route('/users/<id>', methods=['PATCH'])
def update(id):
    user_data = request.get_json()
    msg = validateKeysInUser(user_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg
        }), 406)

    msg1 = validateValueInUser(user_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg1
        }), 406)

    msg2 = validateUserInputType(user_data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 406, 
            'error': msg2
        }), 406)

    user = user_table.get_user_with_id(id)
    print(user)
    if not user:
        return make_response(jsonify({
            'status': 406, 
            'error': 'No user with id:{} was found'.format(id)
        }), 406)
    else:
        updated_user = user_table.update_user(id, user_data)
        print('updated****')
        return make_response(jsonify({
            'status': 201,
            'data': [updated_user]
        }), 201)
        

@user.route('/users/<id>', methods=['DELETE'])
def delete(id): 
    user = user_table.get_user_with_id(id)
    print(user)
    if user:
        print('**deleting**')
        if user_table.delete_user(user):
            print('**deleted**')
            return make_response(jsonify({
                'status': 201,
                'data': {
                    'message': 'user successfully deleted'
                }
            }), 202)
    else:
        return make_response(jsonify({
            'status': 406, 
            'error': 'No user with id:{} was found'.format(id)
        }), 406)

def validateKeysInUser(user):
    if not user:
        return 'No user found'
    elif 'firstname' not in user:
        return 'firstname missing'
    elif 'lastname' not in user:
        return 'lastname missing'
    elif 'email' not in user:
        return 'email missing'
    elif 'phoneNumber' not in user:
        return 'phoneNumber missing'
    elif 'passportUrl' not in user:
        return 'passportUrl missing'
    elif 'isAdmin' not in user:
        return 'isAdmin missing'
    elif 'idNo' not in user:
        return 'idNo missing'
    elif 'username' not in user:
        return 'username missing'
    elif 'password' not in user:
        return 'password missing'
    else:
        return 'ok'

def validateValueInUser(user):
    if not user['firstname'] or len(user['firstname']) < 3:
        return 'firstname missing.\nFirstname must be longer than 2 characters'
    elif not user['lastname'] or len(user['lastname']) < 3:
        return 'lastname missing.\nLastname must be longer than 2 characters'
    elif not user['email'] or len(user['email']) < 3:
        return 'Invalid email.\nEmail must be longer than 2 characters and must contain a @ symbol'
    elif not user['phoneNumber'] or len(user['phoneNumber']) < 10:
        return 'Invalid phoneNumber.\nId No must be 10 characters or longer'
    elif not user['passportUrl'] or len(user['passportUrl']) < 3:
        return 'Invalid passportUrl.\nId No must be longer than 2 characters'
    elif not user['idNo'] or len(user['idNo']) < 3:
        return 'Invalid Id No.\nId No must be longer than 2 characters'
    elif not user['username'] or len(user['username']) < 3:
        return 'Invalid username.\nUsername must be longer than 2 characters'
    elif not user['password'] or len(user['password']) < 3:
        return 'Invalid password.\nPassword must be longer than 2 characters'
    else:
        return 'ok'

def validateUserInputType(user):
    if not user['phoneNumber'].isdigit():
        return 'phoneNumber must be a number'
    elif not isinstance(user['isAdmin'], bool):
        return 'isAdmin must be a boolean'
    elif not user['idNo'].isdigit():
        return 'idNo must be a number'
    else:
        return 'ok'








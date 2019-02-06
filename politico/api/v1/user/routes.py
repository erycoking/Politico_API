from flask import Blueprint, make_response, request, jsonify
from politico.api.v1.user.modal import UserTable

user = Blueprint('user', __name__)

user_table = UserTable()

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
            'data': [user.user_data]
        }), 200)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }), 404)

@user.route('/users', methods=['POST'])
def addUser():
    user_data = request.get_json()
    msg = validate_keys_in_user_data(user_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg
        }), 400)

    msg1 = validate_value_in_user_data(user_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg1
        }), 400)

    msg2 = validate_user_input_type(user_data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg2
        }), 400)

    user1 = user_table.get_user_with_email(user_data['email'])
    if not user1:
        added_user = user_table.add_user(user_data)
        return make_response(jsonify({
            'status': 201,
            'data': [added_user]
        }), 201)
    else:
        return make_response(jsonify({
            'status': 409,
            'error': 'user with email::{} already exists!!!'.format(user_data['email'])
        }), 409)


@user.route('/users/<id>', methods=['PATCH'])
def update(id):
    user_data = request.get_json()
    msg = validate_keys_in_user_data(user_data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg
        }), 400)

    msg1 = validate_value_in_user_data(user_data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg1
        }), 400)

    msg2 = validate_user_input_type(user_data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg2
        }), 400)

    user = user_table.get_user_with_id(id)
    if not user:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }), 404)
    else:
        updated_user = user_table.update_user(id, user_data)
        if not updated_user:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not update user with id:{}'.format(id)
            }), 500)
        else:
            return make_response(jsonify({
                'status': 200,
                'data': [updated_user]
            }), 200)
        

@user.route('/users/<id>', methods=['DELETE'])
def delete(id): 
    user = user_table.get_user_with_id(id)
    if user:
        if user_table.delete_user(id):
            return make_response(jsonify({
                'status': 200,
                'data': {
                    'message': 'user successfully deleted'
                }
            }), 200)
        else:
            return make_response(jsonify({
                'status': 500, 
                'error' : 'Could not delete user with id:{}'.format(id)
            }), 500)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }), 404)

def validate_keys_in_user_data(user):
    if not user:
        return 'No user found'
    elif 'firstname' not in user:
        return 'firstname missing'
    elif 'lastname' not in user:
        return 'lastname missing'
    elif 'email' not in user:
        return 'email missing'
    elif 'phone_number' not in user:
        return 'phone_number missing'
    elif 'passport_url' not in user:
        return 'passport_url missing'
    elif 'is_admin' not in user:
        return 'is_admin missing'
    elif 'id_no' not in user:
        return 'id_no missing'
    elif 'username' not in user:
        return 'username missing'
    elif 'password' not in user:
        return 'password missing'
    else:
        return 'ok'

def validate_value_in_user_data(user):
    if not user['firstname'] or len(user['firstname']) < 3:
        return 'firstname missing.\nFirstname must be longer than 2 characters'
    elif not user['lastname'] or len(user['lastname']) < 3:
        return 'lastname missing.\nLastname must be longer than 2 characters'
    elif not user['email'] or len(user['email']) < 3:
        return 'Invalid email.\nEmail must be longer than 2 characters and must contain a @ symbol'
    elif not user['phone_number'] or len(user['phone_number']) < 10:
        return 'Invalid phone_number.\nId No must be 10 characters or longer'
    elif not user['passport_url'] or len(user['passport_url']) < 3:
        return 'Invalid passport_url.\nId No must be longer than 2 characters'
    elif not user['id_no'] or len(user['id_no']) < 3:
        return 'Invalid Id No.\nId No must be longer than 2 characters'
    elif not user['username'] or len(user['username']) < 3:
        return 'Invalid username.\nUsername must be longer than 2 characters'
    elif not user['password'] or len(user['password']) < 3:
        return 'Invalid password.\nPassword must be longer than 2 characters'
    else:
        return 'ok'

def validate_user_input_type(user):
    if not user['phone_number'].isdigit():
        return 'phone_number must be a number'
    elif not isinstance(user['is_admin'], bool):
        return 'is_admin must be a boolean'
    elif not user['id_no'].isdigit():
        return 'id_no must be a number'
    else:
        return 'ok'








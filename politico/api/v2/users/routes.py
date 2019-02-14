from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.users.model import UserTable

from politico.api.v1.user.routes import validate_keys_in_user_data
from politico.api.v1.user.routes import validate_user_input_type
from politico.api.v1.user.routes import validate_value_in_user_data

user = Blueprint('users', __name__)

user_tb = UserTable()

@user.route('/users', methods=['POST'])
def add_new_user():
    data = request.get_json()
    msg = validate_keys_in_user_data(data)
    if msg != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg
        }), 400)

    msg1 = validate_value_in_user_data(data)
    if msg1 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg1
        }), 400)

    msg2 = validate_user_input_type(data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg2
        }), 400)

    existing_user = user_tb.get_user_with_email(data['email'])
    if not existing_user:
        new_user = user_tb.add_user(data)
        return make_response(jsonify({
            'status': 201,
            'data': [new_user]
        }), 201)
    else:
        return make_response(jsonify({
            'status': 409,
            'error': 'user with email::{} already exists!!!'.format(data['email'])
        }), 409)


@user.route('/users/<int:id>', methods=['GET'])
def get_one(id):
    user = user_tb.get_single_user(id)
    if user != None:
        return make_response(jsonify({
            'status': 200, 
            'data': [user]
        }), 200)
    else:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }), 404)

@user.route('/users', methods=['GET'])
def get_all():
    return make_response(jsonify({
        'status': 200, 
        'data': user_tb.get_all_users()
    }), 200)


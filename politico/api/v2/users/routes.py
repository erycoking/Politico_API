from flask import Blueprint, request, make_response, jsonify
from politico.api.v2.users.model import UserTable

from politico.api.v1.user.routes import validate_keys_in_user_data
from politico.api.v1.user.routes import validate_value_in_user_data

from politico.api.v2.auth.authentication import token_required
from politico.api.v2.auth.authentication import check_if_user_exists

user = Blueprint('users', __name__)

user_tb = UserTable()

@user.route('/users/<int:id>', methods=['GET'])
@token_required
def get_one(current_user, id):
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
@token_required
def get_all(current_user):
    return make_response(jsonify({
        'status': 200, 
        'data': user_tb.get_all_users()
    }), 200)

@user.route('/users/<int:id>', methods=['PATCH'])
@token_required
def update_user(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin) and current_user['id'] != id:
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Please contact admin'
            }), 401)
        
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

    updated_user = user_tb.update_user(id, data)
    if 'error' in updated_user:
        return make_response(jsonify({
            'status': 400,
            'error': updated_user['error']
        }), 400)
    else:
        return make_response(jsonify({
            'status': 200,
            'data': [updated_user]
        }), 200)

    
@user.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    admin = bool(current_user['is_admin'])
    if not (admin):
        print("I am in")
        return make_response(jsonify({
                'status': 401,
                'error': 'Only admin can perform this function'
            }), 401)
    user_exists = user_tb.get_single_user(id)
    if not user_exists:
        return make_response(jsonify({
            'status': 404, 
            'error': 'No user with id:{} was found'.format(id)
        }), 404)   

    if user_tb.delete_user(id):
            return make_response(jsonify({
                'status': 200,
                'data':[{
                    'message': 'user with id:{} deleted'.format(id)
                }]
            }), 200)
    else:
        return make_response(jsonify({
                'status': 400, 
                'error' : 'update or delete on table "users" violates foreign key constraint.\nKey (id)=({}) is referenced on another table'.format(id)
            }), 400)
         
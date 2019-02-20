import jwt
from politico.config import APP_CONFIG
import datetime
from functools import wraps
from flask import Blueprint, redirect, request, make_response, jsonify
from werkzeug.security import check_password_hash

from politico.api.v2.users.model import UserTable

from politico.api.v1.user.routes import validate_keys_in_user_data
from politico.api.v1.user.routes import validate_value_in_user_data

user_tb = UserTable()
auth = Blueprint('auth', __name__)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer.split(' ')[1]

        if not token:
            return make_response(jsonify({
                'status': 403, 
                'error': 'token is missing!!!'
            }), 403)

        try:
            decoded_token = jwt.decode(token, APP_CONFIG['secret'])
            user_id = decoded_token.get('public_id')

            current_user = user_tb.get_single_user(user_id)
            if not current_user:
                return make_response(jsonify({
                    'status': 403, 
                    'error': 'Invalid token!!!'
                }), 403)
        except:
            return make_response(jsonify({
                    'status': 401, 
                    'error': 'Invalid token!!!'
                }), 401)

        return f(current_user, *args, **kwargs)

    return decorated
            



@auth.route('/login', methods=['POST'])
def login():
    credentials = request.authorization

    if not credentials or not credentials.username or not credentials.password:
        return make_response(jsonify({
            'status': 401, 
            'error': 'could not verify'
        }), 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

    user = user_tb.get_user_with_username(credentials.username)
    if not user:
        return make_response(jsonify({
            'status': 401, 
            'error': 'Username or password incorrect'
        }), 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

    if check_password_hash(user['password'], credentials.password):
        token = jwt.encode({'public_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, APP_CONFIG['secret'])
        return make_response(jsonify({
            'status': 200,
            'data': [{
                'token': token.decode('UTF-8'), 
                'user': user
            }]
        }))
    else:
        return make_response(jsonify({
            'status': 401, 
            'error': 'Username or password incorrect'
        }), 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

@auth.route('/signup', methods=['POST'])
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

    msg2 = check_if_user_exists(data)
    if msg2:
        return make_response(jsonify({
            'status': 409,
            'error': msg2
        }), 409)
    else:
        print(user_tb.connection)
        new_user = user_tb.add_user(data)
        if 'error' in new_user:
            return make_response(jsonify({
                'status': 400,
                'error': new_user['error']
            }), 400)
        token = jwt.encode({'public_id': new_user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, APP_CONFIG['secret'])
        return make_response(jsonify({
            'status': 200,
            'data': [{
                'token': token.decode('UTF-8'), 
                'user': new_user
            }]
        }))
        


def check_if_user_exists(data):
    msg = None
    existing_user_with_email = user_tb.get_user_with_email(data['email'])
    existing_user_with_passport_url = user_tb.get_user_with_string('passport_url', data['passport_url'])
    existing_user_with_phone_number = user_tb.get_user_with_int('phone_number', data['phone_number'])
    existing_user_with_id_no = user_tb.get_user_with_int('id_no', data['id_no'])
    existing_user_with_username = user_tb.get_user_with_username(data['username'])

    if existing_user_with_email:
        msg = 'user with email::{} already exists!!!'.format(data['email'])
    elif existing_user_with_passport_url:
        msg = 'user with passport_url::{} already exists!!!'.format(data['passport_url'])
    elif existing_user_with_phone_number:
        msg = 'user with phone_number::{} already exists!!!'.format(data['phone_number'])
    elif existing_user_with_id_no:
        msg = 'user with id_no::{} already exists!!!'.format(data['id_no'])
    elif existing_user_with_username:
        msg = 'user with username::{} already exists!!!'.format(data['username'])
    
    return msg
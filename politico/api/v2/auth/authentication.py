import jwt
import datetime
from functools import wraps
from flask import Blueprint, redirect, request, make_response, jsonify
from werkzeug.security import check_password_hash

from politico.api.v2.users.model import UserTable

from politico.api.v1.user.routes import validate_keys_in_user_data
from politico.api.v1.user.routes import validate_user_input_type
from politico.api.v1.user.routes import validate_value_in_user_data

user_tb = UserTable()
secret_key = 'you_cant_see_me'

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
            decoded_token = jwt.decode(token, secret_key)
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
        token = jwt.encode({'public_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)
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

    msg2 = validate_user_input_type(data)
    if msg2 != 'ok':
        return make_response(jsonify({
            'status': 400, 
            'error': msg2
        }), 400)

    existing_user = user_tb.get_user_with_email(data['email'])
    if not existing_user:
        new_user = user_tb.add_user(data)
        token = jwt.encode({'public_id': new_user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)
        return make_response(jsonify({
            'status': 200,
            'data': [{
                'token': token.decode('UTF-8'), 
                'user': new_user
            }]
        }))
    else:
        return make_response(jsonify({
            'status': 409,
            'error': 'user with email::{} already exists!!!'.format(data['email'])
        }), 409)
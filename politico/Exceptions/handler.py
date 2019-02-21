from flask import Flask, Blueprint, make_response, jsonify
from werkzeug.exceptions import default_exceptions

error = Blueprint('error_handler', __name__)

@error.app_errorhandler(Exception)
def handle_error(err):
    message = str(err)
    # err_list = message.split(' ')
    status_code = 500
    return make_response(jsonify({
            'status': status_code,
            'error': message
        }), status_code)

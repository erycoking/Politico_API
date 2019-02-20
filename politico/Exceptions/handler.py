from flask import Flask, Blueprint, make_response, jsonify
from werkzeug.exceptions import default_exceptions

error = Blueprint('error_handler', __name__)

@error.app_errorhandler(Exception)
def handle_error(err):
    message = [str(x) for x in err.args]
    status_code = err.status_code
    return make_response(jsonify({
            'status': status_code,
            'error': message
        }), status_code)

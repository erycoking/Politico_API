from flask import Flask, Blueprint, make_response, jsonify
from werkzeug.exceptions import default_exceptions

error = Blueprint('error_handler', __name__)

@error.errorhandler
def handle_error(e):
    desc = e.get_description(flask.request.environ)
    return make_response(jsonify({
            'status': e,
            'error': desc
        }), e)

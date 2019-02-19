from flask import Flask, make_response, jsonify
from werkzeug.exceptions import HTTPException

class ExceptionHandler:


    def handle_error(self, e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code

        print(e)
        return make_response(jsonify({
                'status': code,
                'error': str(e)
            }), code)
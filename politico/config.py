""" Initialize the application"""

# import flask
from flask import Flask

# import user blueprint
from politico.api.v1.user.routes import user

# import party blueprint
from politico.api.v1.party.routes import party

# import office blueprint
from politico.api.v1.office.route import office


def create_app():
    # create the app
    app = Flask(__name__)

    # register user blueprint
    app.register_blueprint(user, url_prefix='/api/v1')

    # register party blueprint
    app.register_blueprint(party, url_prefix='/api/v1')

    # register office blueprint
    app.register_blueprint(office, url_prefix='/api/v1')

    return app
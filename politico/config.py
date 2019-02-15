""" Initialize the application"""

# import flask
from flask import Flask

# import blueprints
from politico.api.v1.user.routes import user
from politico.api.v1.party.routes import party
from politico.api.v1.office.route import office
from politico.api.v1.candidate.routes import cand

from configurations.app_config import DevelopmentConfig

def create_app():

    # create the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)

    prefix = '/api/v1'

    # register blueprints
    app.register_blueprint(user, url_prefix=prefix)
    app.register_blueprint(party, url_prefix=prefix)
    app.register_blueprint(office, url_prefix=prefix)
    app.register_blueprint(cand, url_prefix=prefix)

    return app
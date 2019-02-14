""" Initialize the application"""

# import flask
from flask import Flask
from politico.api.v2.db.db import DB

# import blueprints

from politico.api.v1.user.routes import user
from politico.api.v1.party.routes import party
from politico.api.v1.office.route import office
from politico.api.v1.candidate.routes import cand


from politico.api.v2.users.routes import user as user_2
from politico.api.v2.party.routes import party as party_2
from politico.api.v2.office.routes import office as office_2
from politico.api.v2.candidates.routes import cand as cand_2


def create_app():

    db = DB()
    db.initialize_db()

    # create the app
    app = Flask(__name__)

    prefix = '/api/v1'

    # register blueprints for version 1
    app.register_blueprint(user, url_prefix=prefix)
    app.register_blueprint(party, url_prefix=prefix)
    app.register_blueprint(office, url_prefix=prefix)
    app.register_blueprint(cand, url_prefix=prefix)

    prefix_2 = '/api/v2'

     # register blueprints for version 2
    app.register_blueprint(user_2, url_prefix=prefix_2)
    app.register_blueprint(party_2, url_prefix=prefix_2)
    app.register_blueprint(office_2, url_prefix=prefix_2)
    app.register_blueprint(cand_2, url_prefix=prefix_2)


    return app
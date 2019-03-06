""" Initialize the application"""

# import flask
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
from politico.api.v2.db import DB

# import global exception handler
from werkzeug.exceptions import default_exceptions, HTTPException

# import blueprints

from politico.api.v1.user.routes import user
from politico.api.v1.party.routes import party
from politico.api.v1.office.route import office
from politico.api.v1.candidate.routes import cand


from politico.api.v2.users.routes import user as user_2
from politico.api.v2.party.routes import party as party_2
from politico.api.v2.office.routes import office as office_2
from politico.api.v2.candidates.routes import cand as cand_2
from politico.api.v2.vote.routes import vote
from politico.api.v2.petition.routes import petition
from politico.api.v2.auth.authentication import auth
from politico import config
from politico.config import APP_CONFIG
from politico.Exceptions.handler import error

from flask_mail import Mail, Message

mail = ''

def create_app(config):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(APP_CONFIG[config])

    # initializing mailing
    global mail
    mail = Mail(app)

    app.app_context().push()
    # app.config.from_pyfile('config.py')
    
    db = DB()
    db.initialize_db()

    # register error handlers
    app.register_blueprint(error)

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
    app.register_blueprint(vote, url_prefix=prefix_2)
    app.register_blueprint(petition, url_prefix=prefix_2)

    auth_prefix_2 = '/api/v2/auth'

    # register blueprints for auth
    app.register_blueprint(auth, url_prefix=auth_prefix_2)

    return app


def send_mail(user):
    try:
        link = 'https://erycoking.github.io/Politico/UI/user_reset_password.html'

        msg = Message("Reset Password", 
            sender="erycoking360@gmail.com", 
            recipients=[user['email']])
        msg.body = 'Hello '+ user['fullname'] + ', \nYou have requested to reset your password. If you made this request, then please follow this link:'+link
        msg.html = render_template('email_template.html', fullname=user['fullname'], link=link)

        mail.send(msg)

        return 'success'
    except Exception as e:
        print(e)
        return 'fail'

from flask import Flask

app = Flask(__name__)

from politico.api.v1.user.routes import user

app.register_blueprint(user, url_prefix='/api/v1')
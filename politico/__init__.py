from flask import Flask

app = Flask(__name__)

from politico.api.v1.user.routes import user
from politico.api.v1.party.routes import party

app.register_blueprint(user, url_prefix='/api/v1')
app.register_blueprint(party, url_prefix='/api/v1')
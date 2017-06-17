from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from blue.site.routes import mod
from blue.api.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')

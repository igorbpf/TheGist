from flask import Flask

app = Flask(__name__)

from blue.site.routes import mod
from blue.api.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod)
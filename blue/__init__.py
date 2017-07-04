from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['MAIL_SENDER']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = os.environ['MAIL_SENDER']

# Enable cors
CORS(app)

mail = Mail(app)


celery = Celery(app.name, broker=app.config['BROKER_URL'])
celery.conf.update(app.config)


from blue.site.routes import mod
from blue.api.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')

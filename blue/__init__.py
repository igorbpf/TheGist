from flask import Flask
from flask_cors import CORS

from celery import Celery

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


# app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
# app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']

CORS(app)

celery = Celery(app.name, broker=app.config['BROKER_URL'])
celery.conf.update(app.config)


from blue.site.routes import mod
from blue.api.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')

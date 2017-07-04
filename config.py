import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

class StagingConfig(Config):
    DEBUG = False
    DEVELOPMENT = True
    BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

    MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
    MAILGUN_PUBLIC_KEY = os.environ['MAILGUN_PUBLIC_KEY']
    MAILGUN_SMTP_LOGIN = os.environ['MAILGUN_SMTP_LOGIN']
    MAILGUN_SMTP_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
    MAILGUN_SMTP_PORT = os.environ['MAILGUN_SMTP_PORT']
    MAILGUN_SMTP_SERVER = os.environ['MAILGUN_SMTP_SERVER']

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

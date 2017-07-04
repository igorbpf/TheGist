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

    MAIL_DEFAULT_SENDER = os.environ['MAILGUN_SMTP_LOGIN']
    #MAILGUN_PUBLIC_KEY = os.environ['MAILGUN_PUBLIC_KEY']
    MAIL_USERNAME = os.environ['MAILGUN_DOMAIN']
    MAIL_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
    MAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
    MAIL_SERVER = os.environ['MAILGUN_SMTP_SERVER']
    MAIL_USE_TLS = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BROKER_URL = os.environ['REDIS_URL']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

class StagingConfig(Config):
    DEBUG = False
    DEVELOPMENT = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True





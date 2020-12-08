import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'somestupidsecretkeywhichonlyiknow'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # SQLALCHEMY_DATABASE_URI = os.environ['postgresql://tien:123456@127.0.0.1:5432/flask_login']
# postgresql://tien:123456@127.0.0.1:5432/flask_login


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

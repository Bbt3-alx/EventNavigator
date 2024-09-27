import os

class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    """Development environment-specific configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI') or \
        'mysql+pymysql://dev_user:dev_password@localhost/dev_db'


class ProductionConfig(Config):
    """Production environment-specific configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
        'mysql+pymysql://prod_user:prod_password@localhost/prod_db'


class TestingConfig(Config):
    """Testing environment-specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'test_uploads/'

# Map configuration name to the correct config class
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
# -*- encoding: utf-8 -*-


import os
import random
import string

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite3'))

    USE_SQLITE = True 

    # Check if we have environment variables for PostgreSQL
    DB_ENGINE = os.getenv('DB_ENGINE', None)
    DB_USERNAME = os.getenv('DB_USERNAME', None)
    DB_PASS = os.getenv('DB_PASS', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)

    # If PostgreSQL config is provided, use it
    if DB_ENGINE and DB_USERNAME and DB_PASS and DB_HOST and DB_PORT and DB_NAME:
        try:
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            )
            USE_SQLITE = False
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))
            print('> Fallback to SQLite')

    if USE_SQLITE:
        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}

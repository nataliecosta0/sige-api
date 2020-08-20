"""Configuration files of the UPX Reputation Feed API."""

import os
import sys

from datetime import timedelta
from os import path

SECRET_PATH = '/home/natalie/Projects/sige-api/'

if not path.exists(SECRET_PATH):
    SECRET_PATH = os.getcwd()

sys.path.append(SECRET_PATH)

from secret_config import (
    APP_SETTINGS,
    JWT_SECRET_KEY,
    SECRET_KEY,
    SLACK_URL,
    MONGO_USER,
    MONGO_PASS
)


class BaseConfig:
    # flask_bcrypt configuration.
    APP_SETTINGS = APP_SETTINGS
    BCRYPT_LOG_ROUNDS = 12

    DEBUG = False

    # flask_jwt configuration.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_SECRET_KEY = JWT_SECRET_KEY if JWT_SECRET_KEY else 'jwt*super!hard?@secret'

    IP_WHITELIST = ['192.168.58.9']
    SECRET_KEY = SECRET_KEY if SECRET_KEY else 'a_random*very!secret?key'
    SLACK_URL = SLACK_URL


class DevelopmentConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 5
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': '',
        'host': '',
        'port': 0,
        'username': MONGO_USER,
        'password': MONGO_PASS
    }


class TestingConfig(BaseConfig):
    MONGODB_SETTINGS = {
        'db': '',
        'host': '',
        'port': 0,
        'username': MONGO_USER,
        'password': MONGO_PASS
    }


class ProductionConfig(BaseConfig):
    MONGODB_SETTINGS = {
        'db': '',
        'host': '',
        'port': 0,
        'username': MONGO_USER,
        'password': MONGO_PASS
    }
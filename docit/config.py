import logging
from logging import Formatter

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
    LOG_LEVEL=logging.WARNING
    LOG_NAME='/tmp/docit.log'
    LOG_FORMAT=Formatter('%(asctime)s %(levelname)s: %(message)s ')

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'
    LOG_LEVEL=logging.DEBUG
    LOG_NAME='/tmp/docit-dev.log'
    LOG_FORMAT=Formatter('%(asctime)s %(levelname)s [[%(filename)s -> %(funcName)s]]: %(message)s ')

class Testing(Config):
    TESTING = True

# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
HOST = 'localhost'


MONGO_DB_NAME = 'store'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://catalog:c123456@localhost:3306/catalog'
SQLALCHEMY_ECHO = False

CSRF_ENABLED = True
SECRET_KEY = '76g5df67gtts6fdFftdtgssgd7fsrDSGtg6rgih8yffo'

DEBUG = True
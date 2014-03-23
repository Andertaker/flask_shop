# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

CSRF_ENABLED = True
SECRET_KEY = '76g5df67gtts6fdFftdtgssgd7fsrDSGtg6rgih8yffo'

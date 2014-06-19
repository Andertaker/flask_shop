# -*- coding: utf-8 -*-
from flask import render_template, request

from . import app







@app.route('/docs/api')
def docs_api():
    return render_template('api.html')


@app.route('/')
def index():
    return docs_api()

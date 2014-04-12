# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, jsonify, url_for

from app import app, db, models, forms

import database

API_PATH = '/api'


@app.errorhandler(404)
def error404():
    return render_template('404.html'), 404


@app.route('/docs/api')
def docs_api():
    return render_template('api.html')


@app.route('/')
@app.route('/index')
def index():
    category = models.Category.query.filter(
        models.Category.parent.endswith(0)).all()
    return render_template('index.html', categories=category)


#Ниже описан REST api
@app.route(API_PATH + '/category')
def get_category_list():
    if request.is_xhr:
        try:
            return jsonify(response=database.get_category_list()), 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


@app.route(API_PATH + '/category/<int:parent>', methods=['POST'])
def new_category(parent=0):
    if request.is_xhr:
        try:
            req_json = request.form
            database.new_category(parent, req_json['name'], req_json['body'], req_json['alias'])
            return 'created', 201
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 400


@app.route(API_PATH + '/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    if request.is_xhr:
        try:
            req_json = request.form
            database.update_category(category_id, req_json['name'], req_json['body'], req_json['alias'])
            return 'OK', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 400


@app.route(API_PATH + '/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.is_xhr:
        try:
            database.delete_category(category_id)
            return 'Deleted', 200
        except:
            return 'BadRequest', 400
    else:
        return 'Request is not xhr', 404


@app.route(API_PATH + '/category/<int:category_id>/item', methods=['POST'])
def new_item(category_id=0):
    if request.is_xhr:
        try:
            req_json = request.form
            database.new_item(category_id, req_json['name'], req_json['body'], req_json['price'])
            return 'created', 201
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


@app.route(API_PATH + '/category/<int:category_id>/item')
def get_item_list(category_id):
    if request.is_xhr:
        #try:
        return jsonify(response=database.get_item_list(category_id)), 200
        #except:
        #    return 'Bad Request', 400
    else:
        return 'Request is not xhr'


@app.route(API_PATH + '/category/<int:category_id>/item/<int:item_id>')
def get_item(category_id, item_id):
    if request.is_xhr:
        try:
            return jsonify(response=database.get_item(item_id))
        except:
            return 'Bad Request', 400
    else:
        return 'request is not xhr', 404


@app.route(API_PATH + '/category/<int:category_id>/item/<int:item_id>', methods=['PUT'])
def update_item(category_id, item_id):
    if request.is_xhr:
        try:
            req_json = request.form
            database.update_item(item_id, req_json['name'], req_json['body'])
            return 'OK', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


@app.route(API_PATH + '/category/<int:category_id>/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if request.is_xhr:
        try:
            database.delete_item(item_id)
            return 'deleted', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 400
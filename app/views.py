# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, url_for

from app import app

import database

API_PATH = '/api'


@app.errorhandler(404)
def error404(err):
    return render_template('404.html'), 404


@app.route('/docs/api')
def docs_api():
    return render_template('api.html')


@app.route('/category')
def index():
    category = database.get_category_list()
    return render_template('index.html', categories=category)


#обработку ошибок перепишу чуть позже
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
        return 'Request is not xhr', 404


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
        return 'Request is not xhr', 404


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
        try:
            offset = request.args.get('offset', 0, type=int)
            limit = request.args.get('limit', 20, type=int)
            order_by = request.args.get('order_by', 'id', type=str)
            return jsonify(response=database.get_item_list(category_id, offset, limit, order_by)), 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#получение информации по товару в категории
@app.route(API_PATH + '/category/<int:category_id>/item/<int:item_id>')
def get_item(category_id, item_id):
    if request.is_xhr:
        try:
            return jsonify(response=database.get_item(item_id))
        except:
            return 'Bad Request', 400
    else:
        return 'request is not xhr', 404


#обновление товара
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


#удаление айтема
@app.route(API_PATH + '/category/<int:category_id>/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if request.is_xhr:
        try:
            database.delete_item(item_id)
            return 'deleted', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#добавление новой опции
@app.route(API_PATH + '/options', methods=['POST'])
def new_option():
    if request.is_xhr:
        try:
            req_json = request.form
            database.new_option(req_json['name'], req_json['body'], req_json['type'], req_json['alias'])
            return 'Created', 201
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#получение списка опций
@app.route(API_PATH + '/options')
def get_options_list():
    if request.is_xhr:
        try:
            return jsonify(response=database.get_options_list())
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#ообновление опции
@app.route(API_PATH + '/options/<int:option_id>', methods=['PUT'])
def update_option(option_id):
    if request.is_xhr:
        try:
            req_json = request.form
            database.update_option(option_id, req_json['name'], req_json['body'], req_json['type'], req_json['alias'])
            return 'OK', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#Удаление опции
@app.route(API_PATH + '/options/<int:option_id>', methods=['DELETE'])
def delete_option(option_id):
    if request.is_xhr:
        try:
            database.delete_option(option_id)
            return 'deleted', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#Привязка опции к категории
@app.route(API_PATH + '/category/<int:category_id>/options/<int:param_id>', methods=['POST'])
def add_option_to_category(category_id, param_id):
    if request.is_xhr:
        try:
            database.add_option_to_category(category_id, param_id)
            return 'OK', 200
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404


#получает опции заданной категории
@app.route(API_PATH + '/category/<int:category_id>/options')
def get_options_of_category(category_id):
    if request.is_xhr:
        try:
            return jsonify(response=database.get_options_of_category(category_id))
        except:
            return 'Bad Request', 400
    else:
        return 'Request is not xhr', 404
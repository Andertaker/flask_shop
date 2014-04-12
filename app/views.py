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


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/item/<int:item_id>')
def item(item_id):
    items = models.Item.query.get(item_id)
    return render_template('item.html', item=items)


@app.route('/addoption', methods=['GET', 'POST'])
def addoption():
    form = forms.FormAddOption()
    if form.validate_on_submit():
        c = models.CatalogParam(
            name=u'%s' % form.name.data,
            description=u'%s' % form.description.data,
            param_type=u'%s' % form.param_type.data,
            values=u'%s' % form.values.data,
            dimension=u'%s' % form.dimension.data,
            min=u'%s' % form.min.data,
            max=u'%s' % form.max.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('addoption.html', form=form)


@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = forms.FormAddItem()
    if form.validate_on_submit():
        c = models.Item(name=u'' + form.name.data,
                        picture=form.picture.data,
                        description=u'' + form.description.data,
                        price=form.price.data,
                        cat_id=form.cat_id.data,
                        counter_warehouse=form.counter_warehouse.data,
                        counter_shop=form.counter_shop.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('success'))

    return render_template('additem.html', form=form)


def get_ier(category):
    result = []
    temp = category
    while temp.level != 1:
        result.append(temp)
        temp = models.Category.query.get(temp.parent)
    result.append(temp)
    result.reverse()
    return result


@app.route(API_PATH + '/category')
def get_category_list():
    if request.is_xhr:
        return jsonify(response=database.get_category_list()), 200
    else:
        return 'Request is not xhr', 400


@app.route(API_PATH + '/category/<int:parent>', methods=['POST'])
def new_category(parent=0):
    if request.is_xhr:
        req_json = request.form
        database.new_category(parent, req_json['name'], req_json['body'], req_json['alias'])
        return 'Created', 201
    else:
        return 'Request is not xhr', 400


@app.route(API_PATH + '/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    if request.is_xhr:
        req_json = request.form
        database.update_category(category_id, req_json['name'], req_json['body'], req_json['alias'])
        return 'Updated', 200
    else:
        return 'Request is not xhr', 400


@app.route(API_PATH + '/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.is_xhr:
        database.delete_category(category_id)
        return 'Deleted', 200
    else:
        return 'error', 404
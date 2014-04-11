# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, jsonify, url_for
from app import app, db, models, forms
import gets
import json


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


@app.route('/cat/<int:cat_id>')
def cat(cat_id):
    category = models.Category.query.get(cat_id)
    child_categories = models.Category.query.filter(
        models.Category.parent.endswith(cat_id))
    options = [(models.CatalogParam.query.get(x.param_id)) for x in category.options]
    tree_cat = get_ier(category)
    return render_template('cat.html',
                           category=category,
                           child_categories=child_categories,
                           tree_cat=tree_cat, options=options)


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


@app.route('/backend/category')
def get_category_list():
    if request.is_xhr:
        query = models.Category.query.all()
        result = []
        if type(query) != list:
            query = [query]
        for record in query:
            out = {'id': record.id, 'alias': record.alias, 'name': record.name, 'parent': record.parent}
            result.append(out)
        return jsonify(response=result), 200
    else:
        return 'Request is not xhr', 400


@app.route('/backend/category/<int:parent>', methods=['POST'])
def new_category(parent=0):
    if request.is_xhr and request.method == 'POST':
        req_json = request.form
        alias = 'first-category'
        if parent != 0:
            alias = 'sub-category'
        c = models.Category(
            name=u'' + req_json['name'],
            parent=parent,
            description=u'' + req_json['body'],
            alias=u'' + alias
        )
        db.session.add(c)
        db.session.commit()
        return 'Created', 201
    else:
        return 'Request is not xhr', 400


@app.route('/backend/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    req_json = request.form
    c = models.Category.query.get(category_id)
    c.name = req_json['name']
    c.description = req_json['body']
    db.session.commit()
    return 'Updated', 200


@app.route('/backend/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.method == 'DELETE':
        c = models.Category.get(category_id)
        db.session.delete(c)
        db.commit()
        return 'Deleted', 200
    else:
        return 'error', 404
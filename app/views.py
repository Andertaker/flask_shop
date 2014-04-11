# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, jsonify, url_for
from app import app, db, models, forms
import gets
import json


@app.errorhandler(404)
def error404(err):
    return render_template('404.html'), 404


@app.route('/docs/api')
def docs_api():
    return render_template('api.html')


@app.route('/')
@app.route('/index')
def index():
    cat = models.Category.query.filter(
        models.Category.parent.endswith(0)).all()
    return render_template('index.html', categories=cat)


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cat/<int:cat_id>')
def cat(cat_id):
    category = models.Category.query.get(cat_id)
    child_categories = models.Category.query.filter(
        models.Category.parent.endswith(cat_id))
    items = models.Item.query.filter_by(cat_id=cat_id)  # TODO
    options = [(models.CatalogParam.query.get(x.param_id)) for x in category.options]
    tree_cat = get_ier(category)
    return render_template('cat.html',
                           category=category,
                           child_categories=child_categories,
                           tree_cat=tree_cat, options=options)


@app.route('/item/<int:item_id>')
def item(item_id):
    item = models.Item.query.get(item_id)
    return render_template('item.html', item=item)

@app.route('/addoption', methods=['GET', 'POST'])
def addoption():
    form = forms.FormAddOption()
    if form.validate_on_submit():
        c = models.CatalogParam(
            name = u'%s' % form.name.data,
            description = u'%s' % form.description.data,
            param_type = u'%s' % form.param_type.data,
            values = u'%s' % form.values.data,
            dimension = u'%s' % form.dimension.data,
            min = u'%s' % form.min.data,
            max = u'%s' % form.max.data)
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
                        counter_warehouse = form.counter_warehouse.data,
                        counter_shop = form.counter_shop.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('success'))

    return render_template('additem.html', form=form)


def get_option():
    result = []
    result.append(models.OptionsValueText.query.all())
    result.append(models.OptionsValueInt.query.all())
    return result[0] + result[1]

def get_ier(category):
    result = []
    temp = category
    while temp.level != 1:
        result.append(temp)
        temp = models.Category.query.get(temp.parent)
    result.append(temp)
    result.reverse()
    return result

@app.route('/api/<string:method>')
def api(method):
    methods = {
        'category': api_catalog.category,
        'items': api_catalog.item}

    if request.is_xhr:
        dict_of_args = {
            'id': request.args.get('id', None, type=int),
            'parent': request.args.get('parent', None, type=int),
            'options': request.args.get('options', None, type=int),
            'category_id': request.args.get('category_id', None, type=int),
            'min_price': request.args.get('min_price', 0, type=int),
            'max_price': request.args.get('max_price', 9999999, type=int)
        }
        return jsonify(response=methods[method](dict_of_args))
    else:
        return 'NOT AJAX!'


@app.route('/backend/category')
def get_category_list():
    if request.is_xhr:
        query = models.Category.query.all()
        result = []
        if type(query) != list:
            query = [query]
        for record in query:
            out = {}
            out['id'] = record.id
            out['alias'] = record.alias
            out['name'] = record.name
            out['parent'] = record.parent
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
            name = u'' + req_json['name'],
            parent = parent,
            description = u'' + req_json['body'],
            alias = u'' + alias
            )
        db.session.add(c)
        db.session.commit()
        return 'Created', 201
    else:
        return 'Request is not xhr', 400


@app.route('/backend/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    if request.methods = 'PUT':
        req_json = request.form
        c = models.Category.query.get(category_id)
        c.name = req_json['name']
        c.description = req_json['body']
        db.session.commit()
        return 'Updated', 200
    else:
        return 'Not Found', 404


@app.route('/backend/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if request.method == 'DELETE':
        c = models.Category.get(category_id)
        db.session.delete(c)
        db.commit()
        return 'Deleted', 200
    else:
        return 'error', 404
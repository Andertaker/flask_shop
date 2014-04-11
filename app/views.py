# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, jsonify, url_for
from app import app, db, models, forms
import gets
import json
#import api_catalog


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


@app.route('/additem_ajax', methods=['GET', 'POST'])
def additem_ajax():
    if request.is_xhr:
        req_json = json.loads(list(request.form)[0])
        name = req_json['name']
        price = int(req_json['price'])
        description = req_json['description']
        category = int(req_json['category'])
        c = models.Item(name=u'' + name,
                        description=u'' + description,
                        price=price,
                        cat_id=category)
        db.session.add(c)
        db.session.commit()
        item_id = c.id

        #добавляем опцию к айтему
        type_options = ['value_text', 'value_int', 'value_float', 'value_bool']
        for option in req_json['options']:
            param = {'value_text': '', 'value_int': '', 'value_float': 0, 'value_bool': False}
            for t in type_options:
                try:
                    param[t] = req_json['options'][option][t]
                except:
                    pass
            c = models.ParamValue(value_text = u'' + param['value_text'],
                                value_float = param['value_float'],
                                value_int = param['value_int'],
                                value_bool = param['value_bool'],
                                item_id = item_id,
                                param_id = int(option))  
            db.session.add(c)
            db.session.commit()  

        return jsonify(result='succes!')
    else:
        return render_template('additem_ajax.html')


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

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    form = forms.FormAddCategory()
    if form.validate_on_submit():
        if form.parent.data == 0:
            level = 1
        else:
            level = models.Category.query.get(form.parent.data).level + 1
        
        params = [int(x) for x in form.params.data.split('|')]
        print params
        c = models.Category(name=u'%s' % form.name.data,
                            picture=u'%s' % form.picture.data,
                            parent=form.parent.data,
                            level=level
                            )
        db.session.add(c)
        db.session.commit()
        temp = c.id #здесь храним id только что созданной категории
        for param in params:
            c = models.ParamRel(cat_id=temp, param_id=param)
            db.session.add(c)
            db.session.commit()

        return redirect(url_for('success'))
    return render_template('addcat.html', form=form)

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

@app.route('/get', methods=['GET'])
def get():
    types = {'category': gets.category,
            'items': gets.items}
    if request.is_xhr:
        obj = request.args.get('obj', 'undefined', type=str)
        of = request.args.get('of', 'undefined', type=str)
        group_by = request.args.get('group_by', 'undefined', type=id)
        try:
            return jsonify(response=types[obj](of=of, group_by=group_by))
        except:
            return jsonify(response='error')

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




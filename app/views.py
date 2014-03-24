# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, jsonify
from app import app, models, db
import forms

@app.errorhandler(404)
def error404(err):
	return render_template('404.html')

@app.route('/')
@app.route('/index')
def index():
	cat = models.Category.query.filter(
		models.Category.parent.endswith(0)).all()
	return render_template('index.html', categories = cat)

@app.route('/succes')
def succes():
	return render_template('succes.html')

@app.route('/cat/<int:cat_id>')
def cat(cat_id):
	category = models.Category.query.get(cat_id)
	child_categories = models.Category.query.filter(
		models.Category.parent.endswith(cat_id))
	items = models.Item.query.filter_by(cat_id = cat_id)
	tree_cat = get_ier(category)
	return render_template('cat.html', category = category,
		child_categories = child_categories, tree_cat = tree_cat)



@app.route('/item/<int:item_id>')
def item(item_id):
	item = models.Item.query.get(item_id)
	return render_template('item.html', item = item)

@app.route('/addcat', methods = ['GET', 'POST'])
def addcat():
	form = forms.FormAddCat()
	if form.validate_on_submit():
		if form.parent.data == 0:
			level = 1
		else:
			level = models.Category.query.get(form.parent.data).level + 1
		c = models.Category(name = u'' + form.name.data,
			picture = u'' + form.picture.data,
			parent = form.parent.data, level = level)
		db.session.add(c)
		db.session.commit()
		return redirect('/succes')
	return render_template('addcat.html', form = form)

@app.route('/additem', methods = ['GET', 'POST'])
def additem():
	form = forms.FormAddItem()
	if form.validate_on_submit():
		c = models.Item(name = u'' + form.name.data,
			picture = form.picture.data,
			description = u'' + form.description.data,
			price = form.price.data,
			cat_id = form.cat_id.data)
		db.session.add(c)
		db.session.commit()
		return redirect('/succes')

	return render_template('additem.html', form = form)
@app.route('/get/<obj>')
def get(obj):
	if request.is_xhr:

		dict_of_req = {
			'all_cat': [(x.id, x.name) for x in models.Category.query.all()]
		}
		return jsonify(result = dict_of_req[obj])
	else:
		return 'Request is not xhr'
def get_ier(category):
	result = []
	temp = category
	while temp.level != 1:
		result.append(temp)
		temp = models.Category.query.get(temp.parent)
	result.append(temp)
	result.reverse()
	return result
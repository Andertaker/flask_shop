# -*- coding: utf-8 -*-
import models


def category(dict_of_args):
	try:
		if dict_of_args['id'] != None:
			query = models.Category.query.get(dict_of_args['id'])
		elif dict_of_args['id'] == None and dict_of_args['parent'] == None:
			query = models.Category.query.all()
		elif dict_of_args['id'] == None and dict_of_args['parent'] != None:
			query = models.Category.query.filter_by(parent=dict_of_args['parent']).all()
		else:
			query = models.Category.query.all()

		result = []
		for record in query:
			out = {}
			out['name'] = record.name
			out['id'] = record.id
			out['parent'] = record.parent
			result.append(out)
		return result
	except:
		return 'Error'


def item(dict_of_args):
	if dict_of_args['id'] != None:
		query = models.Item.query.get(id)
	elif dict_of_args['category_id'] != None:
		query = models.Item.query.filter_by(cat_id=category_id).filter_by(price<=dict_of_args['max_price']).filter_by(price>=dict_of_args['min_price']).all()
	result = []
	try:
		for record in query:
			out = {}
			out['name'] = record.name
			out['id'] = record.id
			out['price'] = record.price
			out['cat_id'] = record.cat_id
			out['picture'] = record.picture
			out['description'] = record.description
			result.append(out)
		return result
	except:
		return 'Error'
	



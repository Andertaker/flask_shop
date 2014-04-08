# -*- coding: utf-8 -*-
import models

def category(dict_of_args):
	try:
		query = models.Category.query.get(int(dict_of_args['id']))
		result = [{
				'name': query.name, 
				'id': query.id,
				'parent': query.parent
				}]
		return result
	except:
		return 'Error'
	
def category_all(dict_of_args):
	query = models.Category.query.get()
	try:
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
		query = models.Item.query.filter_by(cat_id=category_id)
	result = []
	try:
		for record in query:
			out = {}
			out['name'] = record.name
			out['id'] = record.id
			out['price'] = record.price
			out['cat_id'] = record.cat_id
			out['picture'] = record.picture
			result.append(out)
		return result
	except:
		return 'Error'
	



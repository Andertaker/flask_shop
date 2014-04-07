# -*- coding: utf-8 -*-
#модуль для получения различных данных из бд
import models
def all_options():
    int_options = [(x.id, x.name, x.description) for x in models.OptionsValueInt.query.all()]
    text_options = [(x.id, x.name, x.description) for x in models.OptionsValueText.query.all()]
    float_options = [(x.id, x.name, x.description) for x in models.OptionsValueFloat.query.all()]
    return {'INT': int_options, 'TEXT': text_options, 'FLOAT': float_options}

def options_by_cat_id(id):
	options = [(models.CatalogParam.query.get(x.param_id)) for x in models.Category.query.get(id)]
	return options

def category(of='undefined', group_by='undefined'):
	query = models.Category.query.all()
	result = []
	for record in query:
		out = {}
		out['name'] = record.name
		out['id'] = record.id
		result.append(out)
	return result



def items(of='undefined', group_by='undefined'):
	if of == 'undefined':
		query = models.Item.query.all()
	else:
		query = models.Item.query.filter_by(cat_id=group_by).all()
	result = []
	for record in query:
		out = {}
		out['name'] = record.name
		out['id'] = record.id
		out['parent_id'] = record.cat_id 
		out['description'] = record.description
		out['price'] = record.price
		result.append(out)
	return result
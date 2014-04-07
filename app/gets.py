# -*- coding: utf-8 -*-
#модуль для получения различных данных из бд
import models
from flask import jsonify
def all_options():
    int_options = [(x.id, x.name, x.description) for x in models.OptionsValueInt.query.all()]
    text_options = [(x.id, x.name, x.description) for x in models.OptionsValueText.query.all()]
    float_options = [(x.id, x.name, x.description) for x in models.OptionsValueFloat.query.all()]
    return {'INT': int_options, 'TEXT': text_options, 'FLOAT': float_options}

def options_by_cat_id(id):
	options = [(models.CatalogParam.query.get(x.param_id)) for x in models.Category.query.get(id)]
	return options

def category(of='undefined'):
	result = models.Category.query.all()


def item(of='undefined'):
	if of == 'undefined':
		result = models.Item.query.all()
	else:
		result.models.Item.query.all()

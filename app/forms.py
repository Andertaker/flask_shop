# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, IntegerField, FloatField
from wtforms.validators import Required
import models

class FormAddCat(Form):
	name = TextField('name', validators = [Required()])
	picture = TextField('picture', validators = [Required()])
	cat_list = [(x.id, x.name) for x in models.Category.query.all()]
	cat_list.append((0, u'Нет родителя'))
	parent = SelectField('parent', coerce = int, choices = cat_list)
	
class FormAddItem(Form):
	name = TextField('name', validators = [Required()])
	picture = TextField('picture', validators = [Required()])
	description = TextField('description', validators = [Required()])
	price = IntegerField('price', validators = [Required()])
	cat_list = [(x.id, x.name) for x in models.Category.query.all()]
	cat_id = SelectField('cat_id', validators = [Required()],
		choices = cat_list, coerce = int)

class FormAddOption(Form):
	type_list = [u'text', u'int', u'float', u'checkbox']
	type_list = [(x, x) for x in type_list]
	name = TextField('name')
	description = TextField('description')
	type_option = SelectField('type_option', choices = type_list, coerce = str)
	text_field = TextField('text_field')
	int_field = IntegerField('int_field')
	float_field = FloatField('float_field')
	checkbox = TextField('checkbox')
	unit = TextField('unit') 
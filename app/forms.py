# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, IntegerField
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
	
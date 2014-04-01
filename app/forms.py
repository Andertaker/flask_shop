# -*- coding: utf-8 -*-
import re
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, IntegerField, FloatField, validators as v
import models


class FormAddCategory(Form):
    name = TextField(u'Название категории', validators=[
        v.Required(),
        v.Length(max=64, message=u'Название слишком длинное (максимум 20 символа)'),
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE, message=u'Допускаются буквы, цифры и пробелы'),
    ])
    picture = TextField(u'Изображение категории', validators=[
        v.Optional(),
        v.Regexp('^[a-z0-9]{1}?[a-z0-9\.\-\/]*[a-z0-9]{0,1}$', message=u'Имя файла недопустимо'),
    ])
    cat_list = [(x.id, x.name) for x in models.Category.query.all()]
    cat_list.append((0, u'Нет родителя'))
    parent = SelectField(u'Родительская категория', coerce=int, choices=cat_list)


class FormAddItem(Form):
    name = TextField(u'Название товара', validators=[
        v.Required(),
        v.Length(max=64, message=u'Название слишком длинное (максимум 64 символа)'),
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE, message=u'Допускаются буквы, цифры и пробелы'),
    ])
    picture = TextField(u'Изображение товара', validators=[
        v.Optional(),
        v.Regexp('^[a-z0-9]{1}?[a-z0-9\.\-\/]*[a-z0-9]{0,1}$', message=u'Имя файла недопустимо'),
    ])
    description = TextField(u'Описание', validators=[v.Optional()])
    price = IntegerField(u'Цена', validators=[v.Required()])
    cat_list = [(x.id, x.name) for x in models.Category.query.all()]
    cat_id = SelectField('cat_id', validators=[v.Required()], choices=cat_list, coerce=int)


class FormAddOption(Form):
    type_list = [u'text', u'int', u'float', u'checkbox']
    type_list = [(x, x) for x in type_list]
    name = TextField('name')
    description = TextField('description')
    type_option = SelectField('type_option', choices=type_list, coerce=str)
    text_field = TextField('text_field')
    int_field = IntegerField('int_field')
    float_field = FloatField('float_field')
    checkbox = TextField('checkbox')
    unit = TextField('unit')
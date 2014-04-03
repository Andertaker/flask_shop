# -*- coding: utf-8 -*-
import re
from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, SelectField, IntegerField, FloatField, SelectMultipleField, validators as v
import models
import get

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
    cat_id = SelectField(u'cat_id', validators=[v.Required()], choices=cat_list, coerce=int)


class FormAddOption(Form):
    name = TextField(u'Название', validators = [
        v.Required(),
        v.Length(max=64), 
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE)])
    description = TextField(u'Описание', validators=[
        v.Optional(), 
        v.Length(max=512),
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE)
        ])
    param_type = SelectField(u'param_type', choices=[
        (1, u'Текст'),
        (2, u'Целое число'),
        (3, u'Дробное число'),
        (4, u'Список')
        ])
    values = TextField(u'Список значений', validators = [
        v.Required(),
        v.Length(max=128), 
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE)])
    dimension = TextField(u'Ед. Измерения', validators = [
        v.Required(),
        v.Length(max=8), 
        v.Regexp('^[\w\ \-]+$', flags=re.UNICODE)])
    min = IntegerField(u'Мин.')
    max = IntegerField(u'Макс.')
    to_filter = BooleanField()
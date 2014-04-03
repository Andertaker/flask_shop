# -*- coding: utf-8 -*-
from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    picture = db.Column(db.String(128))
    parent = db.Column(db.Integer)
    level = db.Column(db.Integer)
    items = db.relationship('Item', backref='cat', lazy='dynamic')
    #options = db.relationship('OptionRel', backref='options')

    def __repr__(self):
        print '%s | %s' % (self.id, self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    picture = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        print '%s | %s' % (self.id, self.name)

class CatalogParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    param_type = db.Column(db.Enum, u'Text', u'Integer', u'Float', u'Bool')
    values = db.Column(db.String(256), nullable=True)
    dimension = db.Column(db.String(8))
    min = db.Column(db.Integer, nullable=True)
    max = db.Column(db.Integer, nullable=True)
    to_filter = db.Column(db.Bool)

class ParamRel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    param_id = db.Column(db.Integer)

class ParamValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_text = db.Column(db.String(64))
    value_int = db.Column(db.Integer)
    value_float = db.Column(db.Float)
    value_bool = db.Column(db.Boolean)
    item_id = db.Column(db.Integer)
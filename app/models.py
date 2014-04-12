# -*- coding: utf-8 -*-
from app import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    picture = db.Column(db.String(128))
    parent = db.Column(db.Integer, nullable=False)
    alias = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    level = db.Column(db.Integer)
    items = db.relationship('Item', backref='cat', lazy='dynamic')
    options = db.relationship('ParamRel', backref='pr', lazy='dynamic')

    def __repr__(self):
        print '%s | %s' % (self.id, self.name)


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    picture = db.Column(db.String(128), nullable=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer, deafult=0)
    counter_warehouse = db.Column(db.Integer, default=0)  # кол-во на складе
    counter_shop = db.Column(db.Integer, default=0)  # кол-во в магазине
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        print '%s | %s' % (self.id, self.name)


class CatalogParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    param_type = db.Column(db.Enum(u'Text', u'Integer', u'Float', u'Bool', name='types'))
    values = db.Column(db.String(256), nullable=True)
    dimension = db.Column(db.String(8))
    min = db.Column(db.Integer, nullable=True)
    max = db.Column(db.Integer, nullable=True)
    to_filter = db.Column(db.Boolean)


class ParamRel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    param_id = db.Column(db.Integer)


class ParamValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value_text = db.Column(db.String(64))
    value_int = db.Column(db.Integer)
    value_float = db.Column(db.Float)
    value_bool = db.Column(db.Boolean)
    item_id = db.Column(db.Integer)
    param_id = db.Column(db.Integer)
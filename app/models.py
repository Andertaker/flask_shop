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


class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    type_option = db.Column(db.String)
    text_field = db.Column(db.String(64))
    int_field = db.Column(db.Integer)
    float_field = db.Column(db.Float)
    checkbox = db.Column(db.String(128))
    unit = db.Column(db.String(64))


class OptionRel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_option = db.Column(db.Integer, db.ForeignKey('options.id'))
    id_cat = db.Column(db.Integer, db.ForeignKey('category.id'))


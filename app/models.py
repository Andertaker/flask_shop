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


class OptionRelText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    option_id = db.Column(db.Integer)

class OptionRelInt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer)
    option_id = db.Column(db.Integer)


class OptionsValueText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(64)
    description = db.Column(db.String(512))

class OptionsValueInt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(64)
    description = db.Column(db.String(512))

class OptionsValueFloat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(64)
    description = db.Column(db.String(512))

class OptionsDataText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    options_id = db.Column(db.Integer)
    value = db.Column(db.String)

class OptionsDataInt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    options_id = db.Column(db.Integer)
    value = db.Column(db.Integer)

class OptionsDataFloat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    options_id = db.Column(db.Integer)
    value = db.Column(db.Float)


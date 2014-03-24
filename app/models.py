# -*- coding: utf-8 -*-
from app import db

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	picture = db.Column(db.String(128))
	parent = db.Column(db.Integer)
	items = db.relationship('Item', backref = 'cat',
		lazy = 'dynamic')
	def __repr__(self):
		print '%s | %s' % (self.id, self.name)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64))
	picture = db.Column(db.String(128))
	description = db.Column(db.String(1024))
	price = db.Column(db.Integer)
	cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	def __repr__(self):
		print '%s | %s' % (self.id, self.name)
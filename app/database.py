# -*- coding: utf-8 -*-
from app import models, db


def add_commit(c):
    db.session.add(c)
    db.commit()


def delete_commit(c):
    db.session.delete(c)
    db.commit()


def get_category_list():
    query = models.Category.query.all()
    result = []
    if type(query) != list:
        query = [query]
    for record in query:
        out = {'id': record.id, 'alias': record.alias, 'name': record.name, 'parent': record.parent}
        result.append(out)
    return result


def new_category(parent, name, body, alias):
    c = models.Category(
        name=u'' + name,
        parent=parent,
        description=u'' + body,
        alias=u'' + alias
    )
    add_commit(c)


def update_category(category_id, name, body, alias):
    c = models.Category.query.get(category_id)
    c.name = u'' + name
    c.description = u'' + body
    c.alias = u'' + alias
    db.session.commit()


def delete_category(category_id):
    c = models.Category.query.get(category_id)
    delete_commit(c)


def new_item(category_id, name, body, price):
    c = models.Item(
        cat_id=category_id,
        name=name,
        description=body,
        price=price
    )
    add_commit(c)


def get_item_list(category_id):
    query = models.Item.query.filter_by(cat_id=category_id)
    result = []
    if type(query) != list:
        query = [query]
    for record in query:
        out = {
            'id': record.id,
            'price': record.price,
            'name': record.name,
            'category_id': record.cat_id,
            'description': record.description,
            'counter_warehouse': record.counter_warehouse,
            'counter_shop': record.counter_shop
        }
        result.append(out)
    return result


def get_item(item_id):
    #переписать, чтобы возвращал только если товар есть в указанной категории
    query = models.Item.query.get(item_id)
    out = {
        'id': query.id,
        'price': query.price,
        'name': query.name,
        'category_id': query.cat_id,
        'description': query.description,
        'counter_warehouse': query.counter_warehouse,
        'counter_shop': query.counter_shop
    }
    return out

def update_item(item_id, name, body):
    c = models.Item.query.get(item_id)
    c.name = u'' + name
    c.body = u'' + body
    db.session.commit()

def delete_item(item_id):
    c = models.Item.query.get(item_id)
    delete_commit(c)


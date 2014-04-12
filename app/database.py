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

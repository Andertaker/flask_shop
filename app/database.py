# -*- coding: utf-8 -*-
from app import models, db


def add_commit(c):
    db.session.add(c)
    db.session.commit()


def delete_commit(c):
    db.session.delete(c)
    db.session.commit()


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


def get_item_list(category_id, offset, limit, order_by):
    order_dict = {
        'id': models.Item.id,
        'price': models.Item.price,
        'name': models.Item.name
    }
    query = models.Item.query.filter_by(cat_id=category_id).order_by(order_dict[order_by]).limit(limit).offset(offset)
    #options_of_category = [x.param_id for x in models.ParamRel.query.filter_by(cat_id=category_id)]
    #options_value = models.ParamValue.query.all()
    #print options_value
    rel = models.ParamRel.query.filter_by(cat_id=category_id)

    result = []
    for record in query:

        out = {
            'id': record.id,
            'price': record.price,
            'name': record.name,
            'category_id': record.cat_id,
            'description': record.description,
        }
        result.append(out)
    return result


def options_value(category_id, item_id):
    values = models.ParamValue.query.filter_by(item_id=item_id)
    param = []
    for value in values:
        out = {}
        info = get_options_info(value.param_id)
        if info['type_param'] == 'Integer':
            out['value'] = value.value_int
        elif info['type_param'] == 'Text':
            out['value'] = value.value_text
        elif info['type_param'] == 'Float':
            out['value'] = value.value_float
        else:
            out['value'] = value.value_bool
        out['name'] = value.name
        param.append(out)
    return param

def get_options_info(param_id):
    option = models.CatalogParam.query.get(param_id)
    info = {
        'name': option.name,
        'param_type': option.param_type,
        'alias': option.values,
    }
    return info

def get_item(item_id):
    query = models.Item.query.get(item_id)
    options_value(1,1)
    out = {
        'id': query.id,
        'price': query.price,
        'name': query.name,
        'category_id': query.cat_id,
        'description': query.description,
        'counter_warehouse': query.counter_warehouse,
        'counter_shop': query.counter_shop,
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


def new_option(name, description, param_type, alias):
    c = models.CatalogParam(
        name=u'' + name,
        description=u'' + description,
        param_type=u'' + param_type,
        alias=u'' + alias
    )
    add_commit(c)


def get_options_list():
    query = models.CatalogParam.query.all()
    result = []
    for record in query:
        out = {
            'id': record.id,
            'name': record.name,
            'type': record.param_type,
            'description': record.description,
            'alias': record.alias,
        }
        result.append(out)
    return result


def update_option(option_id, name, description, param_type, alias):
    c = models.CatalogParam.query.get(option_id)
    c.name = u'' + name
    c.description = u'' + description
    c.param_type = u'' + param_type
    c.alias = u'' + alias
    db.session.commit()


def delete_option(option_id):
    c = models.CatalogParam.query.get(option_id)
    delete_commit(c)


def add_option_to_category(category_id, param_id):
    c = models.ParamRel(cat_id=category_id, param_id=param_id)
    add_commit(c)


def get_options_of_category(category_id):
    options_list = [x.param_id for x in models.ParamRel.query.filter_by(cat_id=category_id).all()]
    result = []
    for options_id in options_list:
        query = models.CatalogParam.query.get(options_id)
        out = {
            'id': query.id,
            'description': query.description,
            'alias': query.alias,
            'name': query.name,
            'param_type': query.param_type
        }
        result.append(out)
    return result


def add_option_to_item(category_id, item_id, param_id, value):
    type_of_option = models.CatalogParam.query.get(param_id).param_type

    value_bool = None
    value_float = None
    value_int = None
    value_text = None

    if type_of_option == 'Text':
        value_text = value
    elif type_of_option == 'Integer':
        value_int = value
    elif type_of_option == 'Float':
        value_float = value
    else:
        value_bool = value

    c = models.ParamValue(
        param_id=param_id,
        item_id=item_id,
        value_float=value_float,
        value_int=int(value_int),
        value_text=value_text,
        value_bool=value_bool)
    add_commit(c)
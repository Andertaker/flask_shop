# -*- coding: utf-8 -*-
from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException
from flask.ext.login import current_user

from magazine import app
from models import *

def auth_func(*args, **kw):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!', code=401)


# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
CRUD=['GET', 'POST', 'PUT', 'DELETE']
#cat_excludes = 

def post_get_single(result=None, **kw):
    if "id" in result:
        cat = Category.query.get(result["id"])
        result["children"] = cat.get_children_dict()
        
    return result



"Категории"
manager.create_api(Category, methods=CRUD,
                   #primary_key='slug',
                   exclude_columns=['items', 'level', 'attr_values'],
                   #include_methods = ['get_children_dict']
                   preprocessors={
                       #'GET_SINGLE': [auth_func]  # В разработке
                       },
                   postprocessors={
                       'GET_SINGLE': [post_get_single],
                           },
                   )


"Товары(Продукты)"
manager.create_api(Item, methods=CRUD,
                   #exclude_columns=['cat', 'itemclass', 'attr_values'],
                   include_methods = ['get_attr_values']
                   )


"Атрибуты"
manager.create_api(ItemAtributeValue, methods=CRUD,
                   #include_columns=['testttttt_field', 'value'],
                   )




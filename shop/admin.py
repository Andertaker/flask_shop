# -*- coding: utf-8 -*-
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.model import BaseModelView, InlineFormAdmin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.babelex import Babel

from . import app
from .models import *

babel = Babel(app)

@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'


admin = Admin(app)



class CategoryModelView(ModelView):    
    form_excluded_columns = ['items', 'level']  #, 'parent_id'
    column_exclude_list = ['level']
    
    
class ItemClassAttributeModelView(ModelView):
    form_excluded_columns = ['item_attr_values',] 


class ItemClassModelView(ModelView):
    class ItemClassAttributeInlineModelForm(InlineFormAdmin):
        form_label='Parametres'
        form_excluded_columns = ['item_attr_values',] 
    
    
    form_excluded_columns = ('items', 'attributes')
    inline_models = [ItemClassAttributeInlineModelForm(ItemClassAttribute),]

    
class AttributeOptionGroupModelView(ModelView):
    class AttributeOptionInlineModelForm(InlineFormAdmin):
        form_label='Options'
        form_excluded_columns = ['item_attropt_values',]
    
    form_excluded_columns = ['options', 'classes']
    #inline_models = [(AttributeOption, dict(form_excluded_columns=['item_attropt_values']))]
    inline_models = [AttributeOptionInlineModelForm(AttributeOption),]


class ItemModelView(ModelView):
    form_excluded_columns = ['attr_values',]
    #column_list = ('name', 'cat_id', 'item_class')
    column_labels = dict(name='Name', upc='Article')
    column_exclude_list = ['short_description', 'description']
    column_searchable_list = ['name', 'upc']
    column_filters = ['cat', 'itemclass']
    inline_models = [ItemAtributeValue,]




'''
    * to fix
    , name="Товары"    - уникод не пашет
'''

admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ItemModelView(Item, db.session, name="Products"))
admin.add_view(ItemClassModelView(ItemClass, db.session, name="Product Class"))
admin.add_view(ItemClassAttributeModelView(ItemClassAttribute, db.session, name="Product Class Attribute"))
admin.add_view(AttributeOptionGroupModelView(AttributeOptionGroup, db.session))
#admin.add_view(ModelView(AttributeOption, db.session))
admin.add_view(ModelView(ItemAtributeValue, db.session))










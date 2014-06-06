#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import requests
import random
import json

from magazine.models import Category, Item
from config import HOST



url = 'http://%s:5000/api' % HOST
cat = ['Numizmatika', 'Znachki', 'Bonnistika']
sub_cat = ['Monetyi Rossii', 'Inostrannyie monetyi', 'Monetnyiy brak']

# Drop collection
Category.get_root_categories()


def rand(keys, lst, cat_type):
    if cat_type == 'Category':
        pref_name = cat_type + ' '
    elif cat_type == 'Subcategory':
        pref_name = cat_type + ' '
    d = {}
    if '|' in keys:
        keys = keys.split('|')
    else:
        keys = [keys]
    for k in keys:
        if k == 'name':
            d[k] = pref_name + random.choice(lst)
        else:
            d[k] = random.choice(lst)
    return d



class TestViews(unittest.TestCase):
    # Testing CategoryAPI views

    def setUp(self):
        self.ajax = {
            'X-Requested-With': 'XMLHttpRequest', 
            'content-type': 'application/json'
        }

    def test1(self): # Add category, request is xhr
        r = requests.post(url + '/category', \
            headers=self.ajax, \
            data=json.dumps(rand('alias|name', cat, cat_type='Category'))
        )
        self.assertEqual(r.status_code, 201)

    def test2(self): # Add category, request is not xhr
        r = requests.post(url + '/category', \
            data=json.dumps(rand('alias|name', cat, cat_type='Category'))
        )
        self.assertEqual(r.status_code, 404)

    def test3(self): # Add category with exist field name
        r = requests.post(url + '/category', \
            headers=self.ajax, \
            data=json.dumps(rand('alias', cat, cat_type='Category'))
        )
        self.assertEqual(r.status_code, 400)

    def test4(self): # Get categories list
        r = requests.get(url + '/category', \
            headers=self.ajax
        )
        self.assertEqual(r.status_code, 200)

    def test5(self): # Add category, request is xhr
        for i in range(0, 3):
            r = requests.post(url + '/category', \
                headers=self.ajax, \
                data=json.dumps(rand('alias|name', cat, cat_type='Category'))
            )
            self.assertEqual(r.status_code, 201)

    def test6(self): # Add subcategory, request is xhr
        for i in range(0, 5):
            c = Category.query.filter_by(parent_id=None).first()
            d = rand('name', sub_cat, cat_type='Subcategory')
            r = requests.post(url + '/category/%d' % c.id, \
                headers=self.ajax, \
                data=json.dumps(d)
            )
            self.assertEqual(r.status_code, 201)

    def test7(self): # Get children categories
        p = {'q': 'list'}
        c = Category.query.filter_by(parent_id=None).first()
        r = requests.get(url + '/category/%d' % c.id, \
            headers=self.ajax, \
            params = p
        )
        self.assertEqual(r.status_code, 200)

    def test8(self): # Get single category
        c = Category.query.filter_by(parent_id=None).first()
        r = requests.get(url + '/category/%d' % c.id, \
            headers=self.ajax
        )
        self.assertEqual(r.status_code, 200)

    def test9(self): # Поиск
        #filters = [dict(name='name', op='like', val='%abc%')]
        filters = [dict(name='parent_id', op='is_null')]    #корневые категории
        params = dict(q=json.dumps(dict(filters=filters)))
        
        r = requests.get(url + '/category', \
            headers=self.ajax,
            params=params,
        )
        #print r.json()
        self.assertEqual(r.status_code, 200)
        
    """ 
        Поиск
        http://flask-restless.readthedocs.org/en/latest/searchformat.html
    """
        
        
    def test10(self): # Поиск товаров по атрибутам
        """
            Поиск товаров где Страна производитель = 1
        """    
        
        filters = [dict(name='attr_values', op='any', val={"name":"option_id","op":"==","val":1})]
        params = dict(q=json.dumps(dict(filters=filters)))
        
        #/category/1/items поискать в пределах категории так не получится - выведет все товары
        r = requests.get(url + '/item', \
            headers=self.ajax,
            params=params,
        )
        #print "test10", r.json()
        self.assertEqual(r.status_code, 200)


    def test11(self): # Поиск
        """
            Ищем товар, имеющий параметр Год выпуска (attribute_id =1)
            и значение этого атрибута равное 2014
            
            !!! не пашет
        
        """
        
        
        filters = [dict(name='attr_values', op='any', val={"name":"attribute_id","op":"==","val":1}),
                   dict(name='attr_values', op='any', val={"name":"value_int","op":"==","val":2014})]
        
        params = dict(q=json.dumps(dict(filters=filters)))
        
        r = requests.get(url + '/category', \
            headers=self.ajax,
            params=params,
        )
        print "test11", r.json()
        self.assertEqual(r.status_code, 200)




if __name__ == '__main__':
    unittest.main()

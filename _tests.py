# -*- coding: utf-8 -*-

#from magazine import app
from magazine.models import *

print "roots_cat_number:", len(Category.get_root_categories())



cat_list = Category.query.all()
print cat_list



cat = Category.query.get(3)

#print dir(Category)

print cat.id
#print cat.name
print cat.parent_id

#print dir(cat)
#children = Category.query.filter_by(parent_id=1).all()
#children = cat.query.filter_by(parent_id=cat.id).all()
#print "children", len(children)
#print dir(children)


children = cat.get_children()
print "children", len(children)






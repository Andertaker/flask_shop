
from magazine.models import Item, ItemAtributeValue

#i = Item()
#i.name = "test"

#print i.test_attr

attr = ItemAtributeValue.query.get(1)
#print attr
#print dir(attr)





print dir(ItemAtributeValue)
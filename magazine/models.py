# -*- coding: utf-8 -*-
from magazine import db
from mongoengine import connect, ListField, IntField,FileField 

from config import MONGO_DB_NAME
connect(MONGO_DB_NAME)

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    #picture = db.Column(db.String(128), nullable=True)
    parent_id = db.Column(db.Integer, nullable=True)
    #alias = db.Column(db.String(128), nullable=False)
    #slug = db.Column(db.String(64), nullable=False, unique=True)
    #description = db.Column(db.Text(), nullable=False)
    level = db.Column(db.Integer)
    
    items = db.relationship('Item', backref='cat', lazy='dynamic')
    #options = db.relationship('ParamRel', backref='pr', lazy='dynamic')
    
    @classmethod
    def get_root_categories(cls):
        return cls.query.filter_by(parent_id=None).all()
    
    '''
    def __repr__(self):
        #return '%s | %s' % (self.id, self.name)
        return self.name
    '''
    def __unicode__(self):
        return self.name




    
    def get_children(self):
        children = self.query.filter_by(parent_id=self.id).all()
        return children
        
    def get_children_dict(self):
        children = self.query.filter_by(parent_id=self.id).all()
        
        cats = []
        for c in children:
            cats.append({"id": c.id, "name": c.name})
        
        return cats
        
        

class ItemClass(db.Model):
    __tablename__ = 'itemclass'
    '''
        Класс товара
        например:
            Хододильник
            Футболка
            Книга
    
    '''
    __tablename__ = 'itemclass'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True, nullable=True)
    
    items = db.relationship('Item', backref='itemclass', lazy='dynamic')
    attributes = db.relationship('ItemClassAttribute', backref='itemclass', lazy='dynamic')

    def __repr__(self):
        return self.name

        
class Item(db.Model):
    __tablename__ = 'item'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    upc = db.Column(db.String(64))  #Универсальный Код Товара(Артикул)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    itemclass_id = db.Column(db.Integer, db.ForeignKey('itemclass.id'))
    short_description = db.Column(db.String(255), default="")
    description = db.Column(db.Text())
    #picture = db.Column(db.String(128), nullable=True)
    pictures = ListField(FileField())
    
    "конкретные значения для данного товара"
    attr_values = db.relationship('ItemAtributeValue', backref='item', lazy='dynamic')
    
    def __init__(self):
        self.test_attr = "sdf"
        
        print "item"
        print self.test_attr
        print dir(self)
        
        
    
    def get_attr_values(self):
        #attributes = ItemAtributeValue.query.filter_by(item_id=self.id).all()
        attributes = self.attr_values.all()
        print attributes
        if len(attributes):
            print dir(attributes[0])
        
        #print attributes
        
        
        return {"value": "abc"}
        #attributes = self.query.filter_by(parent_id=self.id).all()
    
    
    ''' 
        Для цены и кол-ва нужны складские записи
    '''
    #price = db.Column(db.Integer)
    #counter_warehouse = db.Column(db.Integer, nullable=True)  # кол-во на складе
    #counter_shop = db.Column(db.Integer, nullable=True)  # кол-во в магазине
    
    def __repr__(self):
        return self.name
    
    



class AttributeOptionGroup(db.Model):
    '''
       Параметры имеющие несколько значений(выбор из списка)
       Пример:
           Страна, Размер, Цвет
    
    '''
    __tablename__ = 'attributeoptiongroup'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    
    options = db.relationship('AttributeOption', backref='attributeoption', lazy='dynamic')
    #типы товаров, в которых используется этот набор(группа) опций
    classes = db.relationship('ItemClassAttribute', backref='optiongroup', lazy='dynamic')  
    
    def __repr__(self):
        return self.name
    
    
class AttributeOption(db.Model):
    '''
        Значения выбора:
            Например "Страна"    -  Россия, США...
            Например "Размер"    Small/Medium/Large
            
    
    '''
    __tablename__ = 'attributeoption'
    
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('attributeoptiongroup.id'), nullable=False)
    
    item_attropt_values = db.relationship('ItemAtributeValue', backref='option', lazy='dynamic')  
    
    def __repr__(self):
        return self.option


class ItemClassAttribute(db.Model):
    '''
        Привязываем тип(класс) товара, к параметрам
        Например для типа Футболка задаются параметры Размер, Цвет...
    
    '''
    __tablename__ = 'itemclass_attribute'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True, nullable=True)
    itemclass_id = db.Column(db.Integer, db.ForeignKey('itemclass.id'), nullable=False)
    type = db.Column(db.Enum(u'Integer', u'Text', u'Option', u'Float', u'Bool', name='types'))
    optiongroup_id = db.Column(db.Integer, db.ForeignKey('attributeoptiongroup.id'))
    ' optiongroup_id используется если type="Option"'
    required = db.Column(db.Boolean, nullable=True)
    to_filter = db.Column(db.Boolean, nullable=True)
    
    item_attr_values = db.relationship('ItemAtributeValue', backref='attribute', lazy='dynamic')  

    def __repr__(self):
        return self.name


class ItemAtributeValue(db.Model):
    '''
        Связь конкретных товаров с конкретными опциями
    
    '''
    __tablename__ = 'item_atributevalue'
    
    id = db.Column(db.Integer, primary_key=True)
    "Товар для которого задаётся значение"
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    "Для какого атрибута задаётся значение т.е. это Масса товара или Год выпуска"
    attribute_id = db.Column(db.Integer, db.ForeignKey('itemclass_attribute.id'), nullable=False)
    value_text = db.Column(db.String(64), nullable=True)
    value_int = db.Column(db.Integer, nullable=True)
    value_float = db.Column(db.Float, nullable=True)
    value_bool = db.Column(db.Boolean, nullable=True)
    option_id = db.Column(db.Integer, db.ForeignKey('attributeoption.id'), nullable=True)


    testttttt_field = "testttttt_val"

    def __repr__(self):
        return str(self.id)

    def __init__(self):
        self.value = "testttttt___init_val"
        self.__dict__["value"] = self.value
        self.__dict__["testttttt_field"] = self.testttttt_field
        
        
        return self
    
    """
    def query(self):
        q = super(ItemAtributeValue, self).query()
        print "query:", q
        self.query = q

        return q
    """
    '''
    def all(self):
        pass
    
    def get(self):
        pass
    '''
    
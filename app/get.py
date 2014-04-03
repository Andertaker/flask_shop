# -*- coding: utf-8 -*-
#модуль для получения различных данных из бд
import models
def all_options():
    int_options = [(x.id, x.name, x.description) for x in models.OptionsValueInt.query.all()]
    text_options = [(x.id, x.name, x.description) for x in models.OptionsValueText.query.all()]
    float_options = [(x.id, x.name, x.description) for x in models.OptionsValueFloat.query.all()]
    return {'INT': int_options, 'TEXT': text_options, 'FLOAT': float_options}
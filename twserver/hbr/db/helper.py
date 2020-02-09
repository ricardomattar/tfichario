# -*- coding: latin1 -*-
"""
Created on Mon Aug 31 06:51:17 2015

@author: ricardo
"""

import datetime

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        #d[column.name] = str(getattr(row, column.name))
        data = getattr(row, column.name)
        if type(data) == datetime.date:
            d[column.name] = data.strftime('%d/%m/%Y')
        elif data == None:
            d[column.name] = ''
        else:
            d[column.name] = unicode(data)

    return d
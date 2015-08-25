# -*- coding: utf-8 -*-

'''
Created on Aug 20, 2015

@author: rcampos
'''
from __future__ import unicode_literals
import csv
import unicodecsv 

class CsvRow:
    ID = 0
    
class Product(CsvRow):
    SHOP_ID=1
    TITLE=2
    POPULARITY=3
    QUANTITY=4
    
class Shop(CsvRow):
    NAME=1
    LAT=2
    LNG=3
    
class Tag(CsvRow):
    TAG=1
    
class Tagging(CsvRow):
    SHOP_ID=1
    TAG_ID=2
    
data_path = 'data/'
def from_csv(name, cbfilter=None, args=None):
    with open(data_path+name+'.csv', 'r') as f:
        reader = unicodecsv.reader(f)
        
        """Condition (row[0] == 'id') assumes all csvs will have a label row with the first cell as 'id'"""
        if cbfilter:
            rows = [row if row[CsvRow.ID] == 'id' or cbfilter(row, args) is True else None for row in reader]
        else:
            rows = [row for row in reader]
            
        rows = filter(None, rows)

        labels = rows[:1][0]
        products = rows[1:]
         
        return [dict(zip(labels, prod)) for prod in products]

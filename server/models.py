# -*- coding: utf-8 -*-

'''
Created on Aug 20, 2015

@author: rcampos
'''
from __future__ import unicode_literals
from server.haversine import haversine_in_meters
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
    

def shop_in_radius_with_taggings(row, args):
    taggings = args['taggings']
    shoptaggings_ids = [tagging['shop_id'] for tagging in taggings]
     
    args = args['geo_args']
    dist = haversine_in_meters(
        float(args['lng']),
        float(args['lat']),
        float(row[Shop.LNG]),
        float(row[Shop.LAT]))
    
    if dist < float(args['radius']) and row[Shop.ID] in shoptaggings_ids:
        return True
    else:
        return False

def shop_in_radius(row, args):
    dist = haversine_in_meters(
        float(args['lng']),
        float(args['lat']),
        float(row[Shop.LNG]),
        float(row[Shop.LAT]))
    
    if dist < float(args['radius']):
        return True
    else:
        return False

def products_in_shops(row, shops):
    shops_ids = [shop['id'] for shop in shops] 
    shopsdict = {shop['id']:shop for shop in shops} 
    
    if row[Product.SHOP_ID] in shops_ids:
        """replace ID with OBJ"""
        row[Product.SHOP_ID] = shopsdict[row[Product.SHOP_ID]]
        return True
    else:
        return False

def tag_exists(row, tags):
    tags = tags.split(',')
    
    if row[Tag.TAG] in tags:
        return True
    else:
        return False

def taggings_exists(row, tags):
    tags_id = [tag['id'] for tag in tags] 
    
    if row[Tagging.TAG_ID] in tags_id:
        return True
    else:
        return False
    
def transform_id_to_object_key(obj, key):
    obj[key] = obj.pop(key+'_id')
    return obj
    
    
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

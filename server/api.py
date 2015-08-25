# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Blueprint, current_app, jsonify, request
from flask.wrappers import Response
from server.haversine import haversine_in_meters
from server.models import from_csv, Shop, Product
import json
import math

api = Blueprint('api', __name__)

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)

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
    
    if row[Product.SHOP_ID] in shops_ids:
        return True
    else:
        return False
    
@api.route('/search', methods=['GET'])
def search():
    """
    receive as GET parameters:
    eg: /search?count=10&radius=500&lat=59.33258&lng=18.0649&tags=trousers%2Cshirts
     
    count: limit the search results
    radius: radius of the search in meters
    lat: global latitude
    lng: global longitude
    tags: tags separated by comma
    """
    shops = from_csv('shops', shop_in_radius, request.args)
    products = from_csv('products', products_in_shops, shops)
 
    """sorts by popularity"""
    products = sorted(products, key=lambda k: k['popularity'], reverse=True)
     
    """limits the results"""
    products = products[:int(request.args['count'])]
    
    #TODO tags filtering
    
#clear debbugging json (not unicode but pretty)
#     response = jsonify({ 'products': products })
#     response.headers.add('Content-Type', 'application/json; charset=utf-8')
    
    response = json.dumps({ 'products': products }, ensure_ascii=False)
    response = Response(response=response)
    
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'

    """Allow access from any other host for now - later we discuss security for this"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

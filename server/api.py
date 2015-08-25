# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Blueprint, current_app, request
from flask.wrappers import Response
from server.models import from_csv, tag_exists, taggings_exists, \
    shop_in_radius_with_taggings, products_in_shops, shop_in_radius
import json

api = Blueprint('api', __name__)

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)
    
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
    
    if 'tags' in request.args and request.args['tags']:
        tags = from_csv('tags', tag_exists, request.args['tags'])
        
        taggings = from_csv('taggings', taggings_exists, tags)
        
        shops = from_csv('shops', shop_in_radius_with_taggings, 
                         { "geo_args": request.args, "taggings": taggings })
    else:
        shops = from_csv('shops', shop_in_radius, request.args)
    
    products = from_csv('products', products_in_shops, shops)
 
    """sorts by popularity"""
    products = sorted(products, key=lambda k: k['popularity'], reverse=True)
     
    """limits the results"""
    products = products[:int(request.args['count'])]
    
    response = json.dumps({ 'products': products }, ensure_ascii=False)
    response = Response(response=response)
    
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'

    """Allow access from any other host for now - later we discuss security for this"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

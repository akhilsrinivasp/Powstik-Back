import json
from urllib import response
from flask import Blueprint, jsonify, request
from .utils import get_all_products, get_product_by_id, products_by_category, add_product, update_product, remove_product
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS


product = Blueprint('product', __name__, url_prefix='/product')

CORS(product)

@product.get('/')
def get_products():
    result=get_all_products()
    if result is None:
       return {"message": "There are 0 products"}, 204
    response =  jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@product.get('/<int:id>')
def get_product(id):
    result = get_product_by_id(id)
    if result is None:
        return {}, 204
    return jsonify(result), 200

@product.get('/bycategory/<string:category_name>')
def get_product_by_category_name(category_name):
    result = products_by_category(category_name)
    if result is None:
           return {"message": "There are 0 products under this category"}, 204
    return json.dumps(result), 200

@product.post('/')
@jwt_required()
def post_product():
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        result = add_product(**res, seller_id=seller_id)
        return result
    return {"message": "Request must be JSON"}, 415
        

@product.patch("/<int:product_id>")
@jwt_required()
def patch_product(product_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        res = request.get_json()
        res["product_id"] = product_id
        result = update_product(**res, seller_id=seller_id)
        return result
    return {"message": "Request must be JSON"}, 415

@product.delete("/<int:product_id>")
@jwt_required()
def delete_product(product_id):
    seller_id = get_jwt_identity()
    res = remove_product(product_id, seller_id=seller_id)
    if res is None:
        return {}, 204
    # return {"message": "Done"}, 200
    return jsonify(res), 200
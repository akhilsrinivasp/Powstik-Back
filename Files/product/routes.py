from flask import Blueprint, jsonify, request
from .utils import get_all_products, get_product_by_id, add_product, update_product, remove_product

product = Blueprint('product', __name__, url_prefix='/product')

@product.get('/')
def get_products():
    result=get_all_products()
    if result is None:
       return {"message": "There are 0 products"}, 204
    return jsonify(result), 200

@product.get('/<int:id>')
def get_product(id):
    result = get_product_by_id(id)
    if result is None:
        return {}, 204
    return jsonify(result), 200

@product.post('/')
def post_product():
    if request.is_json:  
        res = request.get_json()
        result = add_product(**res)
        return result
    return {"message": "Request must be JSON"}, 415
        

@product.patch("/<int:product_id>")
def patch_product(product_id):
    if request.is_json:
        res = request.get_json()
        result = update_product(*product_id, **res)
        if result is None:
            return {}, 204
        return {"message": "Done"}, 202
    return {"message": "Request must be JSON"}, 415

@product.delete("/<int:product_id>")
def delete_product(product_id):
    res = remove_product(product_id)
    if res is None:
        return {}, 204
    return {"message": "Done"}, 200

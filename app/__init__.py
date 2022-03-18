from http import HTTPStatus
from itertools import product
import re
from xxlimited import new
from flask import Flask, jsonify, request

from app.products import (
    read_products_specific_from_csv, 
    read_products_from_csv, 
    validate_keys, 
    write_products_in_csv, 
    rewrite_products_in_csv,
    validate_id)

    
app = Flask(__name__)


@app.get("/products")
def get_products_page():
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page == None or per_page == None:
        products = read_products_specific_from_csv(1, 3)
        return jsonify(products), 200

    products = read_products_specific_from_csv(int(page), int(per_page))
    return jsonify(products), 200


@app.get("/products/<int:product_id>")
def get_products_id(product_id):
    products = read_products_from_csv()
    for product in products:
        print(type(product["id"]))
        if product["id"] == product_id:
            return jsonify(product), 200 

@app.post("/products")
def create_product():
    expected_keys = {"name", "price"}    
    data = request.get_json()
    print(data)
    try:
        validate_keys(data, expected_keys)
    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST

    product = write_products_in_csv(data)

    return jsonify(product), HTTPStatus.CREATED



@app.patch("/products/<int:product_id>")
def patch(product_id:int):
    is_id = validate_id(product_id)
    if is_id != True: 
        return {"error": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND

    data = request.get_json()
    products = read_products_from_csv()
    
    if "price" in data:
        for product in products:
            if product["id"] == product_id:
                product["price"] = data["price"]
            result = product

    if "name" in data:
        for product in products:
            if product["id"] == product_id:
                product["name"] = data["name"]
            result = product
        rewrite_products_in_csv(products)

    return jsonify(result), 200   

@app.delete("/products/<int:product_id>")
def delet_product(product_id):
    products=read_products_from_csv()

    is_id = validate_id(product_id)
    if is_id != True: 
        return {"error": f"product id {product_id} not found"}, HTTPStatus.NOT_FOUND
    
    product_delete = [product for product in products if product["id"] == product_id]
    new_products = [product for product in products if product["id"] != product_id]

    rewrite_products_in_csv(new_products)
    return jsonify(product_delete), HTTPStatus.OK





        
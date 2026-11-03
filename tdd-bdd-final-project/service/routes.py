from flask import Blueprint, jsonify, request
from service import db
from service.models import Product

products = Blueprint("products", __name__)


@products.get("/products")
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    query = Product.query
    if name:
        query = query.filter_by(name=name)
    if category:
        query = query.filter_by(category=category)
    if available is not None:
        query = query.filter_by(available=available.lower() == "true")
    return jsonify([item.serialize() for item in query.all()]), 200


@products.post("/products")
def create_product():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify(error="Product name is required"), 400
    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data.get("price", 0)),
        category=data.get("category", "Other"),
        available=bool(data.get("available", True)),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialize()), 201


@products.get("/products/<int:product_id>")
def read_product(product_id):
    product = Product.find(product_id)
    if product:
        return jsonify(product.serialize()), 200
    return jsonify(error="Product not found"), 404


@products.put("/products/<int:product_id>")
def update_product(product_id):
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415
    product = Product.find(product_id)
    if not product:
        return jsonify(error="Product not found"), 404
    data = request.get_json()
    for field in ("name", "description", "price", "category", "available"):
        if field in data:
            setattr(product, field, data[field])
    db.session.commit()
    return jsonify(product.serialize()), 200


@products.delete("/products/<int:product_id>")
def delete_product(product_id):
    product = Product.find(product_id)
    if not product:
        return "", 404
    db.session.delete(product)
    db.session.commit()
    return "", 204

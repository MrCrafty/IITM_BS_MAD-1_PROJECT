
from flask import Blueprint, jsonify, request
from . import db
from .models import Product, User, Category

api = Blueprint('api', __name__)


@api.route('/getUsers')
def getUsers():
    arr = []
    users = User.query.all()
    for user in users:
        arr.append(user.email)
    return jsonify(arr)


@api.route('/getCategories', methods=["GET", "POST", "DELETE", "PUT"])
def getCategories():
    if (request.method == "POST"):
        data = request.get_json()
        category = Category(categoryName=data["name"])
        db.session.add(category)
        db.session.commit()
        return "Category Successfully added"
    arr = []
    categories = Category.query.all()
    for category in categories:
        item = {}
        item["id"] = category.categoryId
        item["name"] = category.categoryName
        arr.append(item)

    print(arr)
    return "ok"


@api.route('/getProducts', methods=["GET", "POST", "DELETE", "PUT"])
def getProducts():
    if (request.method == "POST"):
        data = request.get_json()
        product = Product(
            productName=data["name"], unit=data["unit"], rate=data["rate"], quantity=data["quantity"], categoryId=data["category"])
        db.session.add(product)
        db.session.commit()
        return "Product Successfully added"
    arr = []
    products = Product.query.all()
    for product in products:
        arr.append(product)
    return jsonify(arr)

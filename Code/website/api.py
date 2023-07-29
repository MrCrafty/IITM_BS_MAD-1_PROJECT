
from flask import Blueprint, jsonify, redirect, request
from . import db
from .models import Product, User, Category

api = Blueprint('api', __name__)


# api for getting all the users

@api.route('/getUsers')
def getUsers():
    arr = []
    users = User.query.all()
    for user in users:
        arr.append(user.email)
    return jsonify(arr)


# api for getting all the categories


@api.route('/getCategories', methods=["GET"])
def getCategories():
    arr = []
    categories = Category.query.all()
    for category in categories:
        item = {}
        item["id"] = category.categoryId
        item["name"] = category.categoryName
        arr.append(item)
    return jsonify(arr)


# api for creating a category


@api.route('/createCategory', methods=["POST"])
def createCategory():
    if (request.method == "POST"):
        data = request.get_json()
        categories = list(Category.query.filter_by(categoryName=data["name"]))
        if (len(categories) > 0):
            return "Category already exists", 500
        category = Category(categoryName=data["name"])
        db.session.add(category)
        db.session.commit()
        return "Category Successfully created", 201

# api for deleting a category


@api.route('deleteCategory', methods=["DELETE"])
def deleteCategory():
    if (request.method == "DELETE"):
        data = request.get_json()
        categories = list(Category.query.filter_by(categoryName=data["name"]))
        if (len(categories) == 0):
            return "Category does not exist", 500
        res = Category.query.filter_by(
            categoryName=data["name"])[0]
        db.session.delete(res)
        db.session.commit()
        print(res)
        return "Category successfully deleted", 200


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

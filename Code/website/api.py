
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
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


# region Category APIs


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


@api.route('/createCategory', methods=["POST", 'GET'])
def createCategory():
    if (request.method == 'POST'):
        data = request.form or request.get_json()
        categories = list(Category.query.filter_by(categoryName=data["name"]))
        if (len(categories) > 0):
            return "<h1>Category already exists</h1><a href='/addcategory'>Go Back</a>", 500
        category = Category(categoryName=data["name"])
        db.session.add(category)
        db.session.commit()
        return "<h1>Category added succesfully</h1><a href='/addcategory'>Add more Categories</a> <a href = '/'>Go to Home page</a>", 201
# api for deleting a category


@api.route('deleteCategory', methods=["DELETE"])
def deleteCategory():
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

# endregion

# region Product APIs


@api.route('/getProducts', methods=["GET"])
def getProducts():
    arr = []
    products = Product.query.all()
    for product in products:
        item = {}
        item["id"] = product.productId
        item["name"] = product.productName
        item["category"] = product.categoryId
        arr.append(item)
    return jsonify(arr)


# api for creating a category


@api.route('/createProduct', methods=["POST"])
def createProduct():
    data = request.get_json()
    categoryId = request.args.get("id", type=int)
    categoryCount = len(Category.query.all())
    if (categoryId is None):
        return "Category Id is null. Please enter category id in url params", 400
    if (categoryId > categoryCount):
        return "Please select valid category", 400
    product = Product(productName=data["name"], unit=data["unit"],
                      rate=data["rate"], quantity=data['quantity'], categoryId=categoryId)
    db.session.add(product)
    db.session.commit()
    return "Product Successfully created", 201

# api for deleting a category


@api.route('deleteProduct', methods=["DELETE"])
def deleteProduct():
    data = request.get_json()
    products = list(Product.query.filter_by(productId=data["id"]))
    if (len(products) == 0):
        return "Product does not exists", 500
    res = products[0]
    db.session.delete(res)
    db.session.commit()
    print(res)
    return "Product Successfully deleted", 200

# endregion

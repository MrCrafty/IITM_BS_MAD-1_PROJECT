
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from . import db
from .models import Product, User, Category
import json

api = Blueprint('api', __name__)


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
        return redirect("/")
# api for deleting a category


@api.route('/deleteCategory', methods=["GET"])
def deleteCategory():
    data = request.args.get("id")
    if (data is None):
        return "Please enter category id in URL"
    products = Product.query.filter_by(categoryId=data).all()
    for product in products:
        db.session.delete(product)
    categories = list(Category.query.filter_by(categoryId=data))
    if (len(categories) == 0):
        return "Category does not exist", 500
    res = categories[0]
    db.session.delete(res)
    db.session.commit()
    db.session.close()

    return redirect("/")


@api.route('/editproduct', methods=['GET', 'POST'])
def UpdateProduct():
    productId = request.args.get('id', type=int)
    data = request.form
    product = Product.query.filter_by(productId=productId).first()
    product.productName = data["name"]
    product.rate = data["rate"]
    product.unit = data["unit"]
    product.quantity = data["quantity"]
    db.session.commit()
    return redirect('/')
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


# api for creating a product


@api.route('/createProduct', methods=["POST"])
def createProduct():
    if (request.method == "POST"):
        data = request.form
        product = Product(productName=data["name"], unit=data["unit"],
                          rate=data["rate"], quantity=data['quantity'], categoryId=data["category"])
        db.session.add(product)
        db.session.commit()
        return redirect("/")

# api for deleting a product


@api.route('deleteProduct', methods=["GET"])
def deleteProduct():
    data = request.args.get("id", type=int)
    products = list(Product.query.filter_by(productId=data))
    if (len(products) == 0):
        return "Product does not exists", 500
    res = products[0]
    db.session.delete(res)
    db.session.commit()

    return redirect("/")

# endregion


@api.route('/addToCart', methods=["GET", "POST"])
def AddToCart():
    productId = request.args.get('id', type=int)
    quantity = request.form["quantity"]
    TotalProducts = Product.query.all()
    IsProduct = False
    for pro in TotalProducts:
        if (pro.productId == productId):
            IsProduct = True
    if (not IsProduct):
        return "Please enter a valid product Id"
    user = current_user
    if (user.is_authenticated and user.role == 'user'):
        user_cart = json.loads((user.cart).replace("\'", "\""))
        if (str(productId) in user_cart.keys()):
            user_cart[str(productId)] += int(quantity)
        else:
            user_cart[str(productId)] = quantity
        user.cart = str(user_cart)
        db.session.commit()
        flash("Added to Cart Successfully", category="success")
        return redirect("/")
    else:
        return "User not authenticated"


@api.route("/deleteFromCart", methods=["GET", "POST"])
def DeleteFromCart():
    productId = request.args.get('id', type=int)
    user = current_user
    if (user.is_authenticated and user.role == "user"):
        user_cart = json.loads((user.cart).replace("\'", "\""))
        del user_cart[str(productId)]
        user.cart = str(user_cart)
        db.session.commit()
        flash("Product deleted from Cart", category="success")
        return redirect("/cart")
    else:
        return "User not authenticated"

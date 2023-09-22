import json
from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user
from .models import Category, Product


views = Blueprint('views', __name__)


@views.route('/')
def Home():
    if (current_user.is_authenticated and current_user.role == "manager"):
        categories = Category.query.all()
        return render_template('Categories.html', categories=categories)
    else:
        categories = Category.query.all()
        return render_template("Home.html", categories=categories)


@views.route('/products')
@login_required
def Products():
    products = Product.query.all()
    category = Category.query.all()
    return render_template('Products.html', products=products, category=category)


@views.route('/addcategory')
@login_required
def AddCategory():
    if (current_user.role == "manager"):
        return render_template('AddCategory.html')
    else:
        return redirect("/")


@views.route('/cart')
@login_required
def Cart():
    user = current_user
    cart = json.loads((user.cart).replace("\'", "\""))
    products = Product.query.all()
    total = 0
    for pro in products:
        if str(pro.productId) in cart.keys():
            if (pro.unit == "$/kg"):
                total += (cart[str(pro.productId)] * int(pro.rate) * 80)
            else:
                total += (cart[str(pro.productId)] * int(pro.rate))
    return render_template('cart.html', cart=cart, products=products, total=total)


@views.route("/addproduct")
def AddProduct():
    if (current_user.role == "manager"):
        categories = Category.query.all()
        return render_template('AddProduct.html', categories=categories)
    else:
        return redirect("/")


@views.route("/editproduct")
def EditProduct():
    productId = request.args.get("id", type=int)
    product = Product.query.filter_by(productId=productId).first()
    categories = Category.query.all()
    return render_template('EditProduct.html', product=product, categories=categories)


@views.route("/addtocart")
def AddToCart():
    productId = request.args.get("id", type=int)
    product = Product.query.filter_by(productId=productId).first()
    print(product)
    return render_template("AddToCart.html", product=product)

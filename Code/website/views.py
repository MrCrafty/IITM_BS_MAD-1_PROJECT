from flask import Blueprint, flash, redirect, render_template
from flask_login import login_required, current_user
from .models import Category, Product


views = Blueprint('views', __name__)


@views.route('/')
def Home():
    categories = Category.query.all()
    return render_template('Home.html', categories=categories)


@views.route('/categories')
@login_required
def Categories():
    categories = Category.query.all()
    return render_template('Categories.html', categories=categories)


@views.route('/products')
@login_required
def Products():
    products = Product.query.all()
    return render_template('Products.html', products=products)


@views.route('/addcategory')
@login_required
def AddCategory():
    if (current_user.role == "manager"):
        return render_template('AddCategory.html')
    else:
        return redirect("/")

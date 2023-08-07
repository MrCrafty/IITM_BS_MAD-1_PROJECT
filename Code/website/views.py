from flask import Blueprint, render_template
from flask_login import login_required
from .models import Category, Product

views = Blueprint('views', __name__)


@views.route('/')
def Home():
    return render_template('Home.html')


@views.route('/loginRequired')
@login_required
def LoginRequired():
    return render_template('Login-Required.html')


@views.route('/categories')
def Categories():
    categories = Category.query.all()
    return render_template('Categories.html', categories=categories)


@views.route('/products')
def Products():
    products = Product.query.all()
    return render_template('Products.html', products=products)


@views.route('/addcategory')
def AddCategory():
    return render_template('AddCategory.html')

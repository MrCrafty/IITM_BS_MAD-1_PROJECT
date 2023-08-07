from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100))


class Category(db.Model):
    categoryId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    categoryName = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product')


class Product(db.Model):
    productId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    productName = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    categoryId = db.Column(db.Integer(), db.ForeignKey(
        'category.categoryId'), nullable=False)

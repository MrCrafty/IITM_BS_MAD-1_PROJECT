from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(100))


class Category(db.Model):
    categoryId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    categoryName = db.Column(db.String(100))
    products = db.relationship(
        'Product', backref=db.backref("product"))


class Product(db.Model):
    productId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    productName = db.Column(db.String(100))
    unit = db.Column(db.String(50))
    rate = db.Column(db.Integer())
    quantity = db.Column(db.Integer())
    categoryId = db.Column(db.Integer(), db.ForeignKey('category.categoryId'))

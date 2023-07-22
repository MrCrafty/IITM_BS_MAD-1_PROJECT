from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(150))
    password = db.Column(db.String(150))


class Category(db.Model):
    categoryId = db.Column(db.Integer(), primary_key=True)
    categoryName = db.Column(db.String(100), relation)


class Product(db.Model):
    productId = db.Column(db.Integer(), primary_key=True)
    productName = db.Column(db.String(100))
    unit = db.Column(db.String(50))
    rate = db.Column(db.Integer(100))
    quantity = db.Column(db.Integer(100))

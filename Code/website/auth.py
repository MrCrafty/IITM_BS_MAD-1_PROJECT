
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import db

from . import DB_NAME
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).all()
        if (user):
            if (len(password) == 0):
                flash("Please enter password")
            else:
                if check_password_hash(user[0].password, password):
                    login_user(user)
                    flash('Login Successful', category='success')
                else:
                    flash("Password is incorrect", category="danger")
        else:
            flash('Email is not registered !', category="danger")
    return render_template('Home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).all()
        if (user):
            flash("Email already exists", category="error")
        else:
            if (len(email) < 4):
                flash("Email is invalid", category="error")
            elif (password != password2):
                flash("Passwords do not match", category="error")
            elif (len(password) < 7):
                flash("Password is very short", category="error")
            else:
                new_user = User(email=email,
                                password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account Successfully created !!", category="success")
            redirect(url_for('views.Home'))

    return render_template('Register.html')


@auth.route('/logout')
@login_required
def logout():
    if (current_user):
        logout_user()
    return redirect(url_for('auth.login'))

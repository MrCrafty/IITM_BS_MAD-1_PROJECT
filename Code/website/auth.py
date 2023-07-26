from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Successful', category='success')
            else:
                flash("Password is incorrect", category="danger")
        else:
            flash('Email is not registered !', category='danger')
    return render_template('Login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if (len(email) < 4):
            flash("Email is invalid", category="error")
        elif (len(firstName) < 2):
            flash("Firstname is too short", category="error")
        elif (password != password2):
            flash("Passwords do not match", category="error")
        elif (len(password) < 7):
            flash("Password is very short", category="error")
        else:
            flash("Account Successfully created !!", category="success")

    return render_template('Register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

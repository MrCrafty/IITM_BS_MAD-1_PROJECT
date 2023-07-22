from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def Home():
    return render_template('Home.html')

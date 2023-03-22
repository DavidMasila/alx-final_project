from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.drinks import Products

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('index.html')


@main.route("/home")
@login_required
def home():
    drink_types = Products.query.all()
    return render_template("home/home.html", 
                           user=current_user.username, 
                           drink_types = drink_types)
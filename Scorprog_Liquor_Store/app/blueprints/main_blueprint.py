from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.drinks import Products
from extensions import admin_permission

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('index.html')


@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Products.query.order_by(Products.name).paginate(page=page, per_page=1)
    return render_template("home/home.html", 
                           user=current_user.username, 
                           pagination = pagination)

@main.route("/<liquor_type>")
@login_required
def drink_type(liquor_type):
    page = request.args.get('page', 1, type=int)
    pagination = Products.query.filter_by(type=liquor_type).paginate(page=page, per_page=1)
    return render_template('products/product.html', pagination=pagination)
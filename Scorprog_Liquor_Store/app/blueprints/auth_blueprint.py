from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.forms.authentication import Signupform, LoginForm
from app.forms.add_product import Liquor
from app.models.users import Client
from app.models.drinks import Products
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from extensions import db, admin_permission, admin_role
from flask_principal import Identity, identity_changed, AnonymousIdentity


auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['GET','POST'])
def signup():
    form = Signupform()
    if form.validate_on_submit():
        email = form.email.data
        client = Client.query.filter_by(email=email).first()
        if not client:
            new_client=Client(firstname=form.firstname.data,
                              lastname=form.lastname.data,
                              email=form.email.data,
                              username=form.username.data,
                              password = generate_password_hash(form.password.data, method='sha256'))
            db.session.add(new_client)
            db.session.commit()
            flash("Account Set up successfully","success")
            return redirect(url_for('auth.login'))
        else:
            flash('That user already exists.')
            return redirect(url_for('auth.login'))
    return render_template('/authentication/signup.html', form=form)

@auth.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if form.validate_on_submit():
        remember = True if request.form.get('remember') else False
        client = Client.query.filter_by(email=form.email.data).first()

        if not client or not check_password_hash(client.password, form.password.data):
            flash("Please check your log in credentials",'danger')
            return redirect(url_for('auth.login'))
        else:
            #get the identity of the user
            identity = Identity(client.id)
            #notify app of the change in identity
            identity_changed.send(current_app._get_current_object(), identity=identity)
            #log in user
            login_user(client, remember=remember)
            return redirect(url_for('main.home'))
    return render_template('authentication/login.html', form=form)

@auth.route("/add_product", methods = ['GET','POST'])
@login_required
@admin_permission.require()
def add_product():
    form = Liquor()
    if form.validate_on_submit():
        new_liqour = Products(name=form.name.data,
                              type = form.type.data,
                              price = int(form.price.data),
                              description = form.description.data,
                              available = form.available.data)
        db.session.add(new_liqour)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('products/add_products.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    logout_user()
    return redirect(url_for('main.index'))

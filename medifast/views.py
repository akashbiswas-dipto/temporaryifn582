from flask import render_template, Blueprint, Flask, request, flash, redirect, url_for, session
from medifast.forms import SignUpForm, LogInForm, OrderForm
from medifast.db import check_for_user, add_user, add_login_record, add_logout_record, get_products, add_order
from medifast.session import get_user, get_shoppingcart,add_to_shoppingcart, shoppingcart_to_order
from .helpers import login_required
from hashlib import sha256
from datetime import datetime
import re

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    products = get_products()
    return render_template('index.html', products=products)

@bp.route("/product")
@login_required
def productDetail():
    return render_template("productdetail.html")

@bp.route("/shoppingcart")
@login_required
def shoppingcart():
    items = get_shoppingcart()
    return render_template("shoppingcart.html", items=items)

@bp.post('/shoppingcart/<int:product_id>/')
@login_required
def add_item_to_shoppingcart(product_id):
    add_to_shoppingcart(product_id)
    return redirect(url_for('main.shoppingcart'))


@bp.post('/shoppingcart/<int:product_id>/<int:quantity>/')
@login_required
def add_item_to_shoppingcart_with_qty(product_id, quantity):
    add_to_shoppingcart(product_id, quantity)
    return redirect(url_for('main.shoppingcart'))

@bp.route("/order", methods=["GET", "POST"])
@login_required
def order():
    form = OrderForm()
    shoppingcart = get_shoppingcart()
    user = get_user()
    if form.validate_on_submit():
        try:
            datetime=datetime.now()
            order = shoppingcart_to_order(form, shoppingcart, user.id, )
            add_order(order)
            return redirect(url_for("main.home"))
        except:
            flash("Server issues. Try again later.")
    elif request.method == "POST":
        print("error:", form.errors)
        flash("Form validation failed.")
    return render_template("main.checkout", shoppingcart=shoppingcart)

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # hash password
        hashed_pw = sha256(password.encode()).hexdigest()
        user = check_for_user(email, hashed_pw)
        print("user", user)
        if not user:
            flash("Email / password is invalid.", "error")
            return redirect(url_for('main.login'))
        session['user'] = {
            'id': user.id,
            'firstname': user.firstname,
            'surname': user.surname,
            'email': user.email,
            'phone': user.phone,
            'username': user.username,
            'user_type': user.user_type,
            'password': ""
        }
        # insert the login time
        add_login_record(user.id)
        flash("Login successfully", "info")
        print("user_id:", get_user())
        return redirect(url_for("main.home"))
    if request.method == "POST":     
        print("Error", form.errors)
        flash("Form validation failed.", 'error')
    return render_template("login.html", form=form)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            password = form.password.data
            # hash password
            hashed_pw = sha256(password.encode()).hexdigest()
            user = check_for_user(form.email.data,hashed_pw)
            if user:
                flash("User already exists", "error")
                return redirect(url_for("main.signup"))
            print(form, hashed_pw)
            add_user(form,hashed_pw)
            flash("Thanks for registering!!!", 'info')
            return redirect(url_for("main.login"))
        except:
            flash("Database issue. Try Later.", "error")
            return redirect(url_for("main.signup"))
    elif request.method == "POST":
        print("Form validation failed:",form.errors)
        flash("Form validation failed.", "error")
    return render_template("signup.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    user = get_user()
    # insert the logout time
    add_logout_record(user.id)
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('main.home'))
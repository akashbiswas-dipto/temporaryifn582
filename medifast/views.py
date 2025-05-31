from flask import render_template, Blueprint, Flask, request, flash, redirect, url_for, session
from medifast.forms import SignUpForm, LogInForm, OrderForm
from medifast.db import check_for_user,admin_check_for_user, add_user, add_login_record,get_product, add_logout_record, get_products, add_order, search
from medifast.session import get_user, get_shoppingcart,add_to_shoppingcart, shoppingcart_to_order, remove_from_shoppingcart, update_item_from_shoppingcart, empty_shoppingcart
from .helpers import login_required
from hashlib import sha256
from datetime import datetime
import re
from collections import defaultdict

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    products = get_products()
    categories= defaultdict(list)
    for product in products:
        categories[product.category].append(product)
    print("category", categories.items())
    return render_template('index.html', categories=categories)

@bp.route("/contact")
def contact():
    return render_template("contact.html")

@bp.route("/search")
def product_search():
    query = request.args.get("query", '').strip()
    results = []
    if query:
        results = search(query)
    categories= defaultdict(list)
    if results:
        for product in results:
            categories[product.category].append(product)
    else:
        categories = None
    return render_template("index.html", categories=categories, query=query)


@bp.route("/product")
@login_required
def productDetail():
    products = get_products()
    categories= defaultdict(list)
    for product in products:
        categories[product.category].append(product)
    return render_template('product.html', categories=categories)


@bp.route("/product/<product_id>")
@login_required
def productDetailByID(product_id):
    product= get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("main.home"))
    return render_template("productdetail.html", product=product )

# shoppingcart page
@bp.route("/cart")
@login_required
def cart():
    cart = get_shoppingcart()
    # check if the cart has item
    if len(cart.items) == 0:
        cart = None
    return render_template("basket.html", cart=cart)


@bp.post('/cart/<int:product_id>/')
@login_required
def add_item_to_shoppingcart(product_id):
    add_to_shoppingcart(product_id)
    return redirect(url_for('main.cart'))


@bp.post('/cart/add')
@login_required
def add_item_to_shoppingcart_with_qty():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    add_to_shoppingcart(product_id, quantity)
    flash("Item added to cart!", "info")
    return redirect(url_for('main.cart'))

@bp.post("/editcartitem/<string:item_id>/")
@login_required
def edit_cartitem(item_id):
    quantity = request.form.get('quantity')
    print("quantity", quantity)
    if quantity == "0" or not quantity.isdigit():
        flash("Quantity cannot be zero or float.", "error")
        return redirect(url_for("main.cart"))
    shoppingcart = get_shoppingcart()
    item = shoppingcart.get_item(item_id)
    print("update cart", item)
    if item:
        flash(f"{item.product.name} has updated.")
        update_item_from_shoppingcart(item_id, int(quantity))
    return redirect(url_for("main.cart"))

# remove cart item route
@bp.post('/removecartitem/<string:item_id>/')
@login_required
def remove_cartitem(item_id):
    shoppingcart = get_shoppingcart()
    item = shoppingcart.get_item(item_id)
    print("remove item", item)  
    if item:
        flash(f"'{item.product.name}' removed from shoppingcart.", "info" )
        remove_from_shoppingcart(item_id)
    else:
        flash("Item not found in shoppingcart.", "error")

    return redirect(url_for('main.cart'))

# empty the whole basket
@bp.route("/empty_cartitem")
@login_required
def empty_cartitem():
    empty_shoppingcart()
    return redirect(url_for('main.cart'))

@bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = OrderForm()
    print("form", form.address.data)
    shoppingcart = get_shoppingcart()
    # check if the cart is empty
    print("shoppingcart", shoppingcart)
    if len(shoppingcart.items) == 0:
        shoppingcart = None
    user = get_user()
    print("user id:", user.id)
    if form.validate_on_submit():
        try:
            order_datetime = datetime.now()
            order = shoppingcart_to_order(form, shoppingcart, user.id, order_datetime)
            print("change to order", order)
            add_order(order)
            empty_shoppingcart()
            return redirect(url_for("main.home"))
        # except TypeError:
            # flash("Type issues. Try again later.", "error")
        except ValueError:
            flash("Value issues. Try again later.", "error")
    elif request.method == "POST":
        print("error:", form.errors)
        flash("Form validation failed.")
    return render_template("checkout.html", cart=shoppingcart, form=form)

@bp.route('/login', methods=["GET","POST"])
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

@bp.route("/admindashboard")
@login_required
def admindashboard():
    user = admin_check_for_user()
    return render_template('admin_panel/index.html',user=user)


@bp.route('/customerdashboard/<int:user_id>')
def customerdashboard(user_id):
    pass
    
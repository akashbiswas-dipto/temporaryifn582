from flask import render_template, Blueprint, Flask, request, flash, redirect, url_for, session
from medifast.forms import SignUpForm, LogInForm
from medifast.db import check_for_user, add_user, get_product
from medifast.session import get_user
from werkzeug.security import generate_password_hash, check_password_hash
from .helpers import login_required
import re

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    products = get_product()
    return render_template('index.html', products=products)

@bp.route("/product")
@login_required
def productDetail():
    return render_template("productdetail.html")

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = check_for_user(form.email.data)
        # print("user", user['password'], user['email'])
        print("user", user)
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Email / password is invalid.", "error")
            return redirect(url_for('main.login'))
        session['user'] = {
            'user_id': user.id,
            'firstname': user.firstname,
            'surname': user.surname,
            'email': user.email,
            'phone': user.phone,
            'username': user.username,
            'role': user.role,
            'password': ""
        }
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
            user = check_for_user(form.email.data)
            if user:
                flash("User already exists", "error")
                return redirect(url_for("main.signup"))
            hashed_pw = generate_password_hash(password) 
            add_user(form,hashed_pw)
            flash("Thanks for registering!!!", 'info')
            return redirect(url_for("main.login"))
        except:
            flash("Database issue. Try Later.", "error")
            return redirect(url_for("main.signup"))
    elif request.method == "POST":
        print("Form validation failed:",form.errors)
        flash("Form validation failed.", "error")
        # if password != confirmPassword:
        #     flash("The password is not the same with confirm password", "error")
        #     return redirect(url_for("main.signup"))
        # if tc == None:
        #     flash("Please click the checkbox.")
        #     return redirect(url_for("main.signup")) 
    return render_template("signup.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('main.home'))
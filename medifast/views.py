from flask import render_template, Blueprint, Flask, request, flash, redirect, url_for, session
from medifast.forms import SignUpForm, LogInForm
from medifast.db import check_for_user, add_user
from medifast.session import get_user
import re

PRIVATE_KEY="medifasthashkey"
emailReg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route("/product")
def productDetail():
    return render_template("productdetail.html")

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        print("email:", form.email.data, "password:", form.password.data)
        hashed_pw = str(hash(PRIVATE_KEY + form.password.data))
        print('hashed_pw', hashed_pw)
        user = check_for_user(form.email.data,  hashed_pw)
        if not user:
            flash("Email / password is invalid.", "error")
            return redirect(url_for('main.login'))
        session['user'] = {
            'user_id': user.id,
            'firstname': user.firstname,
            'surname': user.surname,
            'email': user.email,
            'phone': user.phone,
            'username': user.username
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
            hashed_pw = str(hash(PRIVATE_KEY + password))
            user = check_for_user(form.username.data, hashed_pw)
            if user:
                flash("User already exists", "error")
                return redirect(url_for("main.signup"))             
            add_user(form,hashed_pw)
            flash("Thanks for registering!!!", 'info')
            return redirect(url_for("main.login"))
        except:
            flash("Database issue. Try Later.", "error")
            return redirect(url_for("main.signup"))
    elif request.method == "POST":
        print("Form error:",form.errors)
        flash("Form validation failed.", "error")
        # if password != confirmPassword:
        #     flash("The password is not the same with confirm password", "error")
        #     return redirect(url_for("main.signup"))
        # if tc == None:
        #     flash("Please click the checkbox.")
        #     return redirect(url_for("main.signup")) 
    return render_template("signup.html", form=form)

@bp.route("/logout")
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('main.index'))
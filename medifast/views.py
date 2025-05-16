from flask import render_template, Blueprint, Flask, request, flash, redirect, url_for, session
from medifast.forms import SignUpForm
from medifast.db import check_for_user, add_user
import re


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
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
    return render_template("login.html")

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # check if the user has registered
            print(f"username:", form.username.data, "password:", form.password.data)
            user = check_for_user(form.username.data, form.password.data)
            if user:
                flash("User already exists", "error")
                return redirect(url_for("main.signup"))
            add_user(form)
            flash("Account Signed Up!")
            return redirect(url_for("main.login"))
            # username = request.form.get("username")
            # firstName = request.form.get("firstname")
            # lastName = request.form.get("lastName")
            # email = request.form.get("email")
            # password = request.form.get("password")
            # confirmPassword = request.form.get("confirmPassword")
        # if not re.fullmatch(emailReg, email):
        #     flash("Email format is not right")
        #     return redirect(url_for("main.singup"))
        # if len(password) > 8:
        #     flash("Password allows only 8 characters or digits.", "error")
        #     return redirect(url_for("main.signup"))
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
    session.pop('logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for('main.index'))
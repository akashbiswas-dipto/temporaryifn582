from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return '<a href="/login">Hello World</a>'

@bp.route('/login')
def login():
    return render_template("login.html")

@bp.route("/signup")
def signup():
    return render_template("signup.html")
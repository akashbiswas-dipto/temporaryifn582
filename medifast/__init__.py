from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'ifn582secretKey123@'
    # MySQL configurations
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'ifn582'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)

    bootstrap = Bootstrap(app)
    
    #importing modules here to avoid circular references, register blueprints of routes
    from . import views
    app.register_blueprint(views.bp)
    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
      return render_template("500.html")

    from . import session

    return app
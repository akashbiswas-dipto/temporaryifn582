from flask import Flask

# using this factory setup for the flask application means
# that the app can be run in a test environment
# and with hot reloading.

app = Flask(__name__)

def create_app():
    
    with app.app_context():
        app.debug = False
        # we need to import views so that
        # the routes are registered within the app
        from . import views
        app.register_blueprint(views.bp)

    return app
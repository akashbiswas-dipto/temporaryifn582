from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    From flask document
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
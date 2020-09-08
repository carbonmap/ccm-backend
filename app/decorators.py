from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed == "N":
            flash("Please confirm your account!", "warning")
            return redirect(url_for("auth.unconfirmed"))
        return func(*args, **kwargs)

    return decorated_function

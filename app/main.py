from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from .decorators import confirm_required
from flask import session


main = Blueprint("main", __name__)


@main.route("/")
def index():
    session.clear()
    return render_template("index.html")


@main.route("/admin")
@login_required
@confirm_required
def admin():
    if current_user.admin == "Y":
        return render_template("admin.html")
    else:
        return render_template("index.html")

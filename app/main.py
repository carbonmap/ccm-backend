from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from .decorators import confirm_required

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
@confirm_required
def profile():
    return render_template("profile.html", name=current_user.name, org=current_user.org)

@main.route("/admin")
@login_required
@confirm_required
def admin():
    if current_user.admin == "Y":
        return render_template("admin.html")
    else:
        return render_template("index.html")
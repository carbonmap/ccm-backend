from flask import (
    Flask,
    request,
    send_from_directory,
    render_template,
    Blueprint,
    redirect,
    url_for,
)
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/logout")
def logout():
    return "Logout"


@auth.route("/register", methods=["POST"])
def register_post():
    email = request.form("email")
    name = request.form("name")
    password = request.form("password")

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for("auth.register"))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .admin import updateSqliteTable

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        flash("Invalid email address or password.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))

@auth.route("/register")
def register():
    return render_template("register.html")

@auth.route("/register", methods=["POST"])
def register_post():

    name = request.form.get("name")
    org = request.form.get("org")
    user_type = request.form.get("user_type")
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.register"))

    new_user = User(name=name, org=org, user_type=user_type, email=email, password=generate_password_hash(password, method="sha256"), admin='N')

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/admin", methods=["POST"])
def admin():
    db = "C:/Users/Jeevs/ccm-backend/app/db.sqlite"
    table = "user"
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        if request.form["action"] == "activate":
            updateSqliteTable(db, table, email, "Y")
            flash("Admin privileges successfully added to " + email)
            return redirect(url_for("auth.admin"))
        else:
            updateSqliteTable(db, table, email, "N")
            flash("Admin privileges successfully removed from " + email)
            return redirect(url_for("auth.admin"))
    else:
        flash("The given email address does not match any accounts")
        return redirect(url_for("auth.admin"))

"""
@auth.route("/admin", methods=["POST"])
def admin():
    db = "db.sqlite"
    table = "user"
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        updateSqliteTable("C:/Users/Jeevs/ccm-backend/app/db.sqlite", "user", "jeevan.bhoot@yahoo.com", "Y")
        flash("Admin privileges successfully added to " + email)
        return redirect(url_for("auth.admin"))
    else:
        flash("The given email address does not match any accounts")
        return redirect(url_for("auth.admin"))
"""
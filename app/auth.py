from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from .admin import updateSqliteTable
import datetime
from .email import generate_confirmation_token, confirm_token, send_email
from .decorators import confirm_required
import uuid

import os
app_dir = os.path.dirname(os.path.abspath(__file__))


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.json["email"]
    password = request.json["password"]
    #remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        #flash("Invalid email address or password.")
        #return redirect(url_for("auth.login"))
        status=False
        return jsonify({'result': status})

    login_user(user)
    #session['logged_in'] = True
    status=True
    return jsonify({'result': status})


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    name = request.json["full_name"]
    org = request.json["org"]
    user_type = request.json["user_type"]
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        #flash("Email address already exists")
        #return redirect(url_for("auth.register"))
        status = "Email address already exists"
        return jsonify({'result': status})

    new_user = User(
        id=str(uuid.uuid4()),
        name=name,
        org=org,
        user_type=user_type,
        email=email,
        password=generate_password_hash(password, method="sha256"),
        admin="N",
        registered_on=datetime.datetime.now(),
        confirmed="N",
        confirmed_on=datetime.datetime.now(),
    )

    db.session.add(new_user)
    db.session.commit()

    token = generate_confirmation_token(new_user.email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(new_user.email, subject, html)

    login_user(new_user)

    #flash("A confirmation email has been sent via email", "success")
    #return redirect(url_for("main.index"))
    status = "A confirmation email has been sent via email"
    return jsonify({'result': status})


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/admin", methods=["POST"])
def admin():
    db = f"{app_dir}/db.sqlite"
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


@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired", "danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed == "Y":
        flash("Account already confirmed", "success")
    else:
        user.confirmed = "Y"
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks", "success")
    return redirect(url_for("main.index"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.confirmed == "Y":
        return redirect(url_for("main.index"))
    flash("Please confirm your account", "warning")
    return render_template("unconfirmed.html")


@auth.route("/resend")
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("activate.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent", "success")
    return redirect(url_for("auth.unconfirmed"))

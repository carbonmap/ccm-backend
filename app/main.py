from flask import Flask, request, send_from_directory, render_template, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
def profile():
    return render_template("profile.html")


# Example of a simple page, here at out homepage, as signified by the "/" path
@app.route("/")
def hello_world():
    return render_template("login.html")

<<<<<<< HEAD:app/main.py
from flask import Flask, request, send_from_directory, render_template, Blueprint
=======
from flask import (
    Flask,
    request,
    send_from_directory,
    render_template
)
>>>>>>> 038d069e639c15ac89920a48c07153edcb44479f:hello-world-with-flask/main.py
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD:app/main.py
@main.route('/profile')
def profile():
    return render_template('profile.html')

=======
# Example of a simple page, here at out homepage, as signified by the "/" path
@app.route('/')
def hello_world():
    return render_template("login.html")
>>>>>>> 038d069e639c15ac89920a48c07153edcb44479f:hello-world-with-flask/main.py


from flask import Blueprint, render_template, jsonify, request
import sqlite3
import os, os.path
import shutil
from .admin import sqliteExecute
from . import db

superuser_dashboard = Blueprint("superuser_dashboard", __name__)

limbo_path = "geojson/not_approved"
confirmed_path = "geojson/approved/"
file_name = "some_text.txt"

limbo_list = os.listdir(limbo_path)  # list of all the files limbo folder
confirmed_list = os.listdir(confirmed_path)  # list of all the files limbo folder


@superuser_dashboard.route("/superuser_dashboard")
def super_dash():
    return render_template("super_dash.html")


@superuser_dashboard.route("/showfiles", methods=["POST"])
def show_files():
    limbo_list = os.listdir(limbo_path)
    confirmed_list = os.listdir(confirmed_path)
    data = {"limbo": limbo_list, "confirmed": confirmed_list}
    return jsonify(data)


@superuser_dashboard.route("/movefile", methods=["GET", "POST"])
def Move():

    if request.method == "GET":  # get request left for backend page functionality
        if os.path.isfile(os.path.join(limbo_path, file_name)) == True:
            shutil.move(
                os.path.join(limbo_path, file_name),
                os.path.join(confirmed_path, file_name),
            )

        elif os.path.isfile(os.path.join(confirmed_path, file_name)) == True:
            shutil.move(
                os.path.join(confirmed_path, file_name),
                os.path.join(limbo_path, file_name),
            )

    if request.method == "POST":  # request used in frontend

        name = request.json[
            "name"
        ]  # sets 'name' object to the 'name' of file in json pushed from frontend

        # logic checks which folder the file (with name == name) is in, then moves it to the other folder
        if os.path.isfile(os.path.join(limbo_path, name)) == True:
            shutil.move(
                os.path.join(limbo_path, name), os.path.join(confirmed_path, name)
            )
            toggle_db(name, accept=True)

        elif os.path.isfile(os.path.join(confirmed_path, name)) == True:
            shutil.move(
                os.path.join(confirmed_path, name), os.path.join(limbo_path, name)
            )
            toggle_db(name, accept=False)

        print("The text file has been moved")

    return show_files()


# function toggles the status the file in the database. Takes two arguments: (1) file_name (2) accept=Boolean. Arg (2) allows the same function to be used for accepting or removing file
# the function is called the move request.
def toggle_db(file_name_arg, accept=True):

    name = file_name_arg.split(".geojson")[
        0
    ]  # the id in the db is the file name without the geojson extension.
    # if moving from limbo to confirmed
    if accept == True:
        params = ("accepted", name)
    # if moving from confirmed to limbo
    elif accept == False:
        params = ("submitted", name)

    # Instruction for db accepting params
    instrct = """
                UPDATE reporting_entity SET status = ? WHERE id = ?;
    """
    sqliteExecute(database="db.sqlite", instruction=instrct, params=params)

    print("Database successfully updated")


# Test queries
# UPDATE reporting_entity SET status = 'accepted' WHERE id = 'net.theleys';
# UPDATE reporting_entity SET status = 'submitted' WHERE id = 'net.theleys';

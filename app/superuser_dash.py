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
# limbo_names = [i[1] for i in search_db(approved=False)]
# confirmed_names = [i[1] for i in search_db(approved=True)]


@superuser_dashboard.route("/superuser_dashboard")
def super_dash():
    return render_template("super_dash.html")


@superuser_dashboard.route("/showfiles", methods=["POST"])
def show_files():
    limbo_list = [i[1] for i in search_db(approved=False)]  # set this to the list of human names in the db_search()
    confirmed_list = [i[1] for i in search_db(approved=True)]  # set this to the list of human names in the db_search()
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
        ]  # name from front-end will now be human name from db. Need to obtain id from db and generate filename

        file_name = search_db_name(name=name) + ".geojson"

        # logic checks which folder the file (with name == name) is in, then moves it to the other folder
        if os.path.isfile(os.path.join(limbo_path, file_name)) == True:
            shutil.move(
                os.path.join(limbo_path, file_name),
                os.path.join(confirmed_path, file_name),
            )
            toggle_db(name, accept=True)

        elif os.path.isfile(os.path.join(confirmed_path, file_name)) == True:
            shutil.move(
                os.path.join(confirmed_path, file_name),
                os.path.join(limbo_path, file_name),
            )
            toggle_db(name, accept=False)

        print("The text file has been moved")

    return show_files()


# function obtains the id's and human names from the db
# function called in the show files get request --> human names sent to the front end
# Front end selects human name on dashboard --> human name returned in move_file push request
# Back end matches human name to entity id and uses the toggle_db function to update the db.
# Back end appends ".geojson" to id obtaining physical filename --> current functionality moves physical file


def search_db(approved=True):

    if approved == True:
        params = ("accepted",)
    elif approved == False:
        params = ("submitted",)

    instr = "SELECT id, name FROM reporting_entity WHERE status = ?;"
    search_result = sqliteExecute(
        database="db.sqlite", instruction=instr, params=params
    )
    return search_result


def search_db_name(name):  # searches a entity name in db and returns entity id
    params = (name,)
    instr = "SELECT id FROM reporting_entity WHERE name = ?;"
    search_result = sqliteExecute(
        database="db.sqlite", instruction=instr, params=params
    )
    return search_result[0][0]


# function toggles the status the file in the database. Takes two arguments: (1) file_name (2) accept=Boolean. Arg (2) allows the same function to be used for accepting or removing file
# the function is called the move request.
def toggle_db(human_name, accept=True):

    # if moving from limbo to confirmed
    if accept == True:
        params = ("accepted", human_name)
    # if moving from confirmed to limbo
    elif accept == False:
        params = ("submitted", human_name)

    # Instruction for db accepting params
    instrct = """
                UPDATE reporting_entity SET status = ? WHERE name = ?;
    """
    sqliteExecute(database="db.sqlite", instruction=instrct, params=params)

    print("Database successfully updated")


# Test queries
# UPDATE reporting_entity SET status = 'accepted' WHERE id = 'net.theleys';
# UPDATE reporting_entity SET status = 'submitted' WHERE id = 'net.theleys';

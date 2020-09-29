"""
from flask import Blueprint, render_template, jsonify, request
import os, os.path
import shutil

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
                os.path.join(limbo_path, name),
                os.path.join(confirmed_path, name),
            )

        elif os.path.isfile(os.path.join(confirmed_path, name)) == True:
            shutil.move(
                os.path.join(confirmed_path, name),
                os.path.join(limbo_path, name),
            )

        print("The text file has been moved")

    return show_files()
"""
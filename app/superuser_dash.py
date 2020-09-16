from flask import Blueprint, render_template, jsonify
import os, os.path
import shutil

superuser_dashboard = Blueprint("superuser_dashboard", __name__)

limbo_path = "test_data/limbo_state/"
confirmed_path = "test_data/confirmed_state/"
file_name = "some_text.txt"

limbo_list = os.listdir(limbo_path)  # list of all the files limbo folder
confirmed_list = os.listdir(confirmed_path)  # list of all the files limbo folder


@superuser_dashboard.route("/superuser_dashboard")
def super_dash():
    return render_template(
        "super_dash.html"
    )


@superuser_dashboard.route("/showfiles", methods=['POST'])
def show_files():
    limbo_list=os.listdir(limbo_path)
    confirmed_list=os.listdir(confirmed_path)
    data = {'limbo' : limbo_list, 'confirmed' : confirmed_list}
    return jsonify(data)


@superuser_dashboard.route("/movefile", methods=['POST'])
def Move():
    # function checks which folder the file is in, then moves it to the other folder

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

    print("The text file has been moved")

    return show_files()
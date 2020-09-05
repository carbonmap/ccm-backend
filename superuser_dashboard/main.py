from flask import Flask, render_template, request, jsonify
import os, os.path
import shutil

app = Flask(__name__)

limbo_path = "superuser_dashboard/limbo_state/"
confirmed_path = "superuser_dashboard/confirmed_state/"
file_name = "some_text.txt"

limbo_list = os.listdir(limbo_path)  # list of all the files limbo folder
confirmed_list = os.listdir(confirmed_path)  # list of all the files limbo folder


@app.route("/")
def home():
    return render_template(
        "home.html", limbo_list=limbo_list, confirmed_list=confirmed_list
    )


@app.route("/ShowFiles")
def ShowFiles():
    return render_template("show_files.html", limbo_list=os.listdir(limbo_path), confirmed_list=os.listdir(confirmed_path))
    

@app.route("/SomeFunction")
def SomeFunction():
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
    
    return ShowFiles()


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import os, os.path

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/SomeFunction')
def SomeFunction(): 
    # function checks which folder the file is in, then moves it to the other folder
    
    if os.path.isfile('superuser_dashboard/limbo_state/some_text.txt') == True:
        os.rename('superuser_dashboard/limbo_state/some_text.txt', 'superuser_dashboard/confirmed_state/some_text.txt')
        
    elif os.path.isfile('superuser_dashboard/confirmed_state/some_text.txt') == True:
        os.rename('superuser_dashboard/confirmed_state/some_text.txt', 'superuser_dashboard/limbo_state/some_text.txt')
    
    print('The text file has been moved')
    return "Nothing"

if __name__ == "__main__":
    app.run(debug=True)
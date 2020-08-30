from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__)

# Allow some funky stuff with requesting from other localhosts (in our case requesting files from our Angular.js server)
CORS(app)

# Example of a simple page, here at out homepage, as signified by the "/" path
@app.route("/")
def hello_world():
    return render_template("login.html")


# Example of using parameters in the url, which may be used for finding entities
@app.route("/hello")
def give_name():
    name = request.args.get("name")
    if not name:
        return "Hi! add '?name=<name>' to the url to get a funky message!"
    else:
        return f"Hi, {name}!"


# Examples of getting data from directories using Flask
@app.route("/geojson/<path:path>")
def getGeojson(path):
    return send_from_directory("geojson", path)


@app.route("/reporting_entities/<path:path>")
def getDatajson(path):
    return send_from_directory("reporting_entities", path)

@app.route("/login", methods=["POST"])
def login():
    loginData = request.get_json()
    email = loginData['email']
    password = loginData['password']
    print(email, password)
    if len(password) > 24:
        return '{"Response" : "Password is greater than 24 chars"}' #just an example of logic that can be used to determine the server response.
    #perform hash comparison here and return appropriate response
    
    return '{"Response" : "OK"}'


# Run this file to start the *development* server
if __name__ == "__main__":
    app.run(port=8080)

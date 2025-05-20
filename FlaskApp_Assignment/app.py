from flask import Flask, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re


load_dotenv()


MONGO_URI = os.getenv('MONGO_URI')

#create mongo client to use the connection
client = MongoClient(MONGO_URI)

#specify the db to work upon
db = client["flask_demo"]

#use this collection or pass collection on runtime
collection = db["users"]


app = Flask(__name__)

@app.route("/")
def render_form():
    # render the form template on root route
    return render_template("form.html")


def validate_form(name, email):
    errors = []
    if not name.replace(" ", "").isalpha():
        errors.append("Name: must be contain alphabets only")
    # We can add multiple validate according to our requirement
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Email: must be a valid email")
    return errors


@app.route("/submit", methods=["POST"])
def submit_form_data():
    # Check for the form data validation (strip to check empty spaces in input)
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()

    errors = validate_form(name, email)

    if errors:
        # stay on same page and show error in template
        return render_template('form.html', errors=errors, name=name, email=email)
    else:
        # add data to mongo and redirect
        try:
            user = {
                name: name,
                email: email
            }
            collection.insert_one(user)
        except Exception as e:
            errors.clear()
            errors.append(e)
            return render_template('form.html', errors=errors, name=name, email=email)
        return redirect(url_for("success"))

@app.route("/success")
def success():
    # render success template
    return render_template("success.html")

@app.route("/api")
def get_file_data():
    try:
        #open the json file in read mode and read the data of file
        with open("data_list.json", "r") as file:
            file_data = file.read()
        # return data in json format
        return json.loads(file_data)
    except:
        # suppose if there are any issues with either operation this will be displayed
        return json.dumps({"message": "Exception: Something bad happened"})


if __name__ == "__main__":
    app.run(debug=True)

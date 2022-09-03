from flask import request, render_template, redirect, Flask
from flask_mail import Mail, Message
import os
import re
from cs50 import SQL
from flask_session import Session

app = Flask("__name__")
db = SQL("sqlite:///database.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return redirect("/login")
    elif request.method == "POST":
        return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")

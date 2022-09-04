from flask import request, render_template, redirect, Flask, session
from flask_mail import Mail, Message
import os
import re
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask("__name__")
db = SQL("sqlite:///database.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def index():
    try:
        session["user_id"]
    except:
        return redirect("/login")
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", eror=False)
    elif request.method == "POST":
        username = request.form.get("user_name")
        password = request.form.get("password")
        email = request.form.get("email")
        name = request.form.get("name")
        hashpass = generate_password_hash(password)
        user = db.execute("SELECT user_name FROM users")
        emailss = db.execute("SELECT email FROM users")
        users = []
        emails = []
        error = False
        user_feedback = "valid-feedback"
        user_validity = "is-valid"
        email_feedback = "valid-feedback"
        email_validity = "is-valid"
        for item in user:
            users.append(item["user_name"])
        for item in emailss:
            emails.append(item["email"])

        if username in users:
            error = True
            user_feedback = "invalid-feedback"
            user_validity = "is-invalid"
        if email in emails:
            error = True
            email_feedback = "invalid-feedback"
            email_validity = "is-invalid"
        if error:
            return render_template("register.html", eror=True, user_feedback=user_feedback, user_validity=user_validity,
                                   email_validity=email_validity, email_feedback=email_feedback, name=name,
                                   username=username, email=email, password=None)
        else:
            db.execute("INSERT INTO users (user_name, hashpass, email, name) VALUES (?, ?, ?, ?)", username, hashpass, email, name)
            id = db.execute("SELECT user_id FROM users WHERE user_name=?", username)[0]
            user_id = id["user_id"]
            session["user_id"] = user_id
            return redirect("/")

        # db.execute("INSERT INTO users (user_name, hashpass, email, name)VALUES (?, ?, ?, ?)", username, hashpass, email, name)

from flask import request, render_template, redirect, Flask, session
from flask_mail import Mail, Message
import os
import re
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask("__name__")
db = SQL("sqlite:///database.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# email configuring
app.config["MAIL_DEFAULT_SENDER"] = "a.mortazaie.uk@outlook.com"
app.config["MAIL_PASSWORD"] = "amirali.1388"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "a.mortazaie.uk@outlook.com"
mail = Mail(app)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        users = db.execute("SELECT * FROM users WHERE user_name = ?", user_name)

        if len(users) != 1 or not check_password_hash(users[0]["hashpass"], password):
            return render_template("login.html", eror=True, user_validity="is-invalid",
                                   user_feedback="invalid-feedback")
        else:
            user_id = users[0]["user_id"]
            session["user_id"] = user_id
            return redirect("/")
    else:
        return render_template("login.html", eror=False)


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
            message = Message(f"You are registered!", recipients=[email],
                              body=f"Hi {name}    You are registered in todo, \n"
                                   f"welcome")
            mail.send(message)
            db.execute("INSERT INTO users (user_name, hashpass, email, name) VALUES (?, ?, ?, ?)", username, hashpass,
                       email, name)
            id = db.execute("SELECT user_id FROM users WHERE user_name=?", username)[0]
            user_id = id["user_id"]
            session["user_id"] = user_id
            return redirect("/")

        # db.execute("INSERT INTO users (user_name, hashpass, email, name)VALUES (?, ?, ?, ?)", username, hashpass, email, name)


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")


@app.route("/changepass", methods=["POST", "GET"])
@login_required
def changepass():
    if request.method == "POST":
        password = request.form.get("password")
        hashpass = generate_password_hash(password)
        db.execute("UPDATE users SET hashpass=? WHERE user_id = ?", hashpass, session["user_id"])
        email = db.execute("SELECT email FROM users WHERE user_id = ?", session["user_id"])[0]["email"]
        name = db.execute("SELECT name FROM users WHERE user_id = ?", session["user_id"])[0]["name"]
        message = Message(f"TODO password change", recipients=[email],
                          body=f"Hi {name}\n    Your password successfully changed")
        mail.send(message)
        return redirect("/")
    else:
        return render_template("changepass.html")
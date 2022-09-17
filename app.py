from flask import request, render_template, redirect, Flask, session
from flask_mail import Mail, Message
import os
from datetime import datetime
import re
import datetime
import sqlite3
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


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            status = db.execute("SELECT status FROM tasks WHERE task_id = ?", id)[0]["status"]
        except:
            return render_template("index.html", id = id)

        if status == "TODO":
            db.execute("UPDATE tasks SET status = 'DONE' WHERE task_id = ?", id)
        else:
            db.execute("UPDATE tasks SET status = 'TODO' WHERE task_id = ?", id)
        return redirect("/")
    else:
        return redirect("/changepass")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        if request.form.get("name"):
            db.execute("UPDATE FROM tasks WHERE i")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        if len(db.execute("SELECT * FROM types WHERE user_id == ?", session["user_id"])) == 0:
            db.execute("INSERT INTO types (user_id, type) VALUES (?, ?)", session["user_id"], "main")
        type = db.execute("SELECT type FROM types WHERE user_id = ?", session["user_id"])

        today = datetime.date
        now = int(str(datetime.datetime.now())[8:10])
        tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
        for item in tasks:
            if int(item["day"]) < now and item["status"] == "DONE":
                db.execute("DELETE FROM tasks WHERE task_id = ?", item["task_id"])
        task = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY day", session["user_id"])
        return render_template("index.html", today=today, types=type, tasks=task)
    else:
        if request.form.get("date") == "":
            a = datetime.datetime
            date = str(a.now())[:-7]
        else:
            date = request.form.get("date")
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        hour = date[11:13]
        minute = date[14:16]

        name = request.form.get("name")
        ttype = request.form.get("type")
        db.execute("INSERT INTO tasks (user_id, task_name, day, month, year, hour, minute, status, type, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name, day, month, year, hour, minute, "TODO", ttype, date)

        return redirect("/")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    tid = request.form.get("id")
    db.execute("DELETE FROM tasks WHERE user_id = ? AND task_id = ?", session["user_id"], tid)
    return redirect("/")


@app.route("/ntype", methods=["POST", "GET"])
@login_required
def ntype():
    newType = request.form.get("nametype")
    types = db.execute("SELECT type FROM types WHERE type = ? AND user_id = ?", newType, session["user_id"])
    if len(types) == 0 and len(newType) > 0:
        db.execute("INSERT INTO types (user_id, type) VALUES (?, ?)", session["user_id"], newType)
        return redirect("/")
    else:
        return redirect("/")

@app.route("/dltype", methods=["POST", "GET"])
@login_required
def dltype():
    newType = request.form.get("nametype")
    types = db.execute("SELECT type FROM types WHERE type = ? AND user_id = ?", newType, session["user_id"])
    if len(types) == 1 and newType:
        db.execute("DELETE FROM types WHERE type = ? AND user_id = ?", newType, session["user_id"])
        return redirect("/")
    else:
        return redirect("/logout")


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

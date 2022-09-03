from flask import request, render_template, redirect, Flask
from flask_mail import Mail, Message
import os
import re

app = Flask("__name__")

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return redirect("/login")
    return render_template("index.html")
from flask import request, render_template, redirect, Flask
from flask_mail import Mail, Message
import os
import re

app = Flask("__name__")



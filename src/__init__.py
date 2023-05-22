from flask import Flask, session
from flask_session import Session

web_app = Flask("src")
web_app.config["SESSION_PERMANENT"] = False
web_app.config["SESSION_TYPE"] = "filesystem"
Session(web_app)
from src.controllers import *

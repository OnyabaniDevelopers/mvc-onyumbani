from flask import Flask

web_app = Flask("src")

from src.controllers import *

"""
    Example Controllers
"""

from src import web_app
from flask import render_template, redirect, url_for

# Import model(s)
from src.models.Homes import Home

#route index
@web_app.route('/', methods = ['GET'])
def index():
    # load data in models
    data = Home.get_home()

    return render_template('index.html.j2', data = data)

"""
    Example Controllers
"""

from src import web_app
from flask import render_template, redirect, url_for, request, session
import os
import firebase_admin
from firebase_admin import credentials, storage
import time

# Import model(s)
from src.models.Homes import Home
from src.models.FirebaseAuth import Authentication


#route index
@web_app.route('/')
def index():
    '''Index page controller'''
    # return render_template('index.html.j2')
    return render_template('image_upload.html.j2')

@web_app.route('/login', methods =['GET', 'POST'])
def login():
    '''Logging in controller'''
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email = request.form['email']
        password = request.form['password']

        user = Authentication.login(email, password)

        if str(user.status) == '200':

            # save session data
            session['loggedin'] = True
            session['id'] = email

            msg = 'Logged in successfully !'
            return redirect(url_for('index'))
        
        else:

            msg = 'Incorrect username / password !'

    return render_template('login.html.j2', msg = msg)
   
@web_app.route('/upload', methods=['POST'])
def upload():
    return render_template('index.html.j2')
    
#TODO: Fix the FileNotFoundError
'''
Initialize Firebase Admin SDK
cred = credentials.Certificate(os.path.abspath("service_key_onyumbani.json"))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'onyumbanihousing-1cc4d.appspot.com'
})
bucket = storage.bucket()

@web_app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file found", 400

    image = request.files['image']
    if image.filename == '':
        return "Invalid file", 400

    filename = f"profile_{int(time.time() * 1000)}{os.path.splitext(image.filename)[1]}"
    blob = bucket.blob(filename)
    blob.upload_from_file(image)

    # Set the URL expiration time to 1 hour
    url = blob.generate_signed_url(expiration=3600)
    print(url)

    return redirect(url_for('index'))
'''
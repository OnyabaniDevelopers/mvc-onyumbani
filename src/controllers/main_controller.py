import time
from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing

from src.models.Homes import Homes

@web_app.route('/upload', methods=['POST'])
def upload():

    # getting image from the request
    image = request.files['image']
    
    url = ImageProcessing.upload_img(image)
    
    print(url)
    
    return redirect(url_for('index'))


# clear session of closing browser
@socketio.on('disconnect')
def clear_session():
    SessionProcessing.clear_session(session)
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('userId', None)
    session.pop('usertype', None)


#route index
@web_app.route('/')
def index():
    '''Index page controller'''

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    all_homes = Homes.get_homes()

    return render_template('index.html.j2', data=tabs, homes=all_homes)
    

@web_app.route('/about')
def about():
    '''About page controller'''

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    all_homes = Homes.get_homes()

    return render_template('about.html.j2', data=tabs, homes=all_homes)




    




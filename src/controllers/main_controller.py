import time
from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import send_email
from src.models.Students import Students
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing

from src.models.Homes import Homes
from src.models.Hosts import Hosts

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
@web_app.route('/index')
@web_app.route('/')
def index():
    '''Index page controller'''
    session['currentpage'] = 'index'

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    all_homes = Homes.get_homes()

    return render_template('index.html.j2', data=tabs, homes=all_homes)
    # return render_template('map.html')

@web_app.route('/view_profile')
def view_profile():
    
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    profile_data = {}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}
        userId = session['userId']
        tabs['add_home'] = 'Add Home' 
        if session['usertype'] == 'owner':
           tabs['add_home'] = 'Add Home'
           profile_data = Hosts.get_host(userId)  
           
        else:
             tabs['add_home'] = ""
             profile_data = Students.get_student(userId) 
             
        if 'profileimg' not in profile_data:
                profile_data['profileimg'] = url_for('static', filename='pics/profile.png')

    return render_template('viewprofile.html.j2', data=tabs, profile_data=profile_data)

@web_app.route('/about', methods=['GET', 'POST'])
def about():
    '''About page controller'''
    msg=""

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    all_homes = Homes.get_homes()

    if request.method == 'POST' and request.form['senderemail'] and request.form['sendername']\
    and request.form['message']:
        
        send_email(request.form['senderemail'], request.form['message'], request.form['sendername'])
        msg="Message was sent successfully"
        # return redirect('/about#contactForm', about_msg=msg)
        return render_template('about.html.j2', data=tabs, homes=all_homes, about_msg=msg)

    return render_template('about.html.j2', data=tabs, homes=all_homes, about_msg=msg)

# endpoint to view otheer users profile e.g student viewing owner or owner viewing student
@web_app.route('/view_profile/<usertype>/<userId>')
def view_profile_all(userId, usertype):
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    profile_data = {}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}
        tabs['add_home'] = 'Add Home'

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else "" 

    if usertype == 'owner':
        profile_data = Hosts.get_host(userId)  
    else:
        profile_data = Students.get_student(userId) 
        
    if 'profileimageurl' not in profile_data:
        profile_data['profileimageurl'] = url_for('static', filename='pics/profile.png')
    
    return render_template('viewprofile2.html.j2', data=tabs, profile_data=profile_data)



    




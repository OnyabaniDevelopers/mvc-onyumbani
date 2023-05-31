import time
from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import send_email
from src.models.Students import Students
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing
from src.models.FirebaseAuth import Authentication
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
    msg = ''
    color = ''

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    all_homes = Homes.get_homes()
    
    if 'msg' in request.args:
        msg = request.args.get('msg')
        color = request.args.get('color')

    return render_template('index.html.j2', msg=msg, color=color, data=tabs, homes=all_homes)
    # return render_template('map.html')

@web_app.route('/view_profile')
def view_profile():
    log = ' '
    color = ' '
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
                
        if 'log' in request.args:
            log = request.args.get('log')
            color = request.args.get('color')
    
        return render_template('viewprofile.html.j2', data=tabs, profile_data=profile_data, log=log, color=color)
     
    msg = "Please Log in first"
    return redirect(url_for('login', msg=msg))


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

    
@web_app.route('/updateprofile', methods =['GET','POST'])
def updateprofile():
    msg=' '
    color = '#FF3062'
    url = ''
    del_pic =''
    
    if 'loggedin' in session and session['usertype']:
        if request.method == 'POST' and request.form['firstname'] and request.form['homeaddress']\
              and request.form['lastname'] and request.form['bio']\
              and request.form['phonenumber']:
              
            user_data = {}
            for entry, value in request.form.to_dict().items():
                user_data[entry] = value
                
            if 'profileimage' in request.files and request.files['profileimage'].filename != '':
                url = ImageProcessing.upload_img(request.files['profileimage'])
                user_data['profileimg'] = url
                
                if session['usertype'] == 'owner':
                    response0 = Hosts.get_host(session['userId'])
                elif session['usertype'] == 'student':
                    response0 = Students.get_student(session['userId'])
                    
                if 'profileimg' in response0:
                    del_pic = response0['profileimg']
                
            user_data['nationalId'] = session['userId']
            
            if session['usertype'] == 'owner':
                response = Hosts.update_host(user_data, user_data['nationalId'])
            elif session['usertype'] == 'student':
                response = Students.update_student(user_data, user_data['nationalId'])
            
            if response == 200:
                msg = 'Successfully updated'
                color = 'green'
                
                if del_pic:
                    SessionProcessing.clear_session_images({'profileimg':del_pic})
                
                return redirect(url_for('view_profile', log=msg, color=color))
                
            if url:
                SessionProcessing.clear_session_images({'profileimg':url})                
                            
            msg = '*Sorry, Failed to create account'
            return redirect(url_for('view_profile', msg=msg, color=color))
            
        elif request.method == 'POST':
            msg = '*Sorry, some required information are missing'     
            return redirect(url_for('view_profile', log=msg, color=color))
    else:
        msg = "Please Log in first"
        return redirect(url_for('login', msg=msg,))


@web_app.route('/delete', methods =['GET'])
def delete():
    msg = ' '
    
    if 'loggedin' in session and session['loggedin'] == True:
        delete_user_response = Authentication.delete_user(session['idToken'])

        if delete_user_response == 200:
            if session['usertype'] == 'owner':
                response = Hosts.delete_host(session['userId'])
            elif session['usertype'] == 'student':
                response = Students.delete_student(session['userId'])
                
            if response == 200:
                msg='Delete successful'
                return redirect(url_for('login', log=msg))
         
        msg='Failed to delete'
        return redirect(url_for('view_profile', log=msg, color='#FF3062'))
        
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
    
    
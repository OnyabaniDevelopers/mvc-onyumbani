import time
from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing
from src.models.FirebaseAuth import Authentication
from src.models.Students import Students
from src.models.Hosts import Hosts
from src.models.Homes import Homes


@web_app.route('/login', methods =['GET', 'POST'])
def login():
    '''Logging in controller'''

    msg = ' '

    #log out user
    if 'loggedin' in session and session['loggedin'] == True:
            # save session data
            session['loggedin'] = False
            session.pop('email', None)
            session.pop('userId', None)
            session.pop('usertype', None)
            
            msg = 'Logged out successfully !'
            return redirect(url_for('index'))


    if request.method == 'POST' and request.form['email'] and request.form['password']:
        email = request.form['email']
        password = request.form['password']

        user = Authentication.login(email, password)
        print(user.status)

        if str(user.status) == '200':
            user_info = Authentication.get_user_info(email)
            
            for key, value in user_info.items():
                session[key] = value

            # save session data
            session['loggedin'] = True
        

            msg = 'Logged in successfully !'
            return redirect(session['currentpage'])
        
        else:
            msg = 'Incorrect username / password !'
    elif request.method == 'POST':
        msg = '*Fill all fields'
    
    return render_template('login.html.j2', log = msg)

'''
Signing in process
'''
    
@web_app.route('/sign_up_one', methods =['GET', 'POST'])
def sign_up_one():
    msg=' '
    if request.method == 'POST' and request.form['password'] and request.form['confirmpassword']\
        and request.form['lastname'] and request.form['firstname'] and request.form['homeaddress']\
            and request.form['dob'] and request.form['usertype'] and request.form['email']\
                and request.form['password'] == request.form['confirmpassword']:
        # save session data

        for entry, value in request.form.to_dict().items():
            session[entry] = value

        if 'profileimage' in request.files and request.files['profileimage'].filename != '':
            url = ImageProcessing.upload_img(request.files['profileimage'])
            session['profileimg'] = url

            
        return redirect(url_for('sign_up_two'))
    elif request.method == 'POST':
        msg = '*Sorry, some required information are missing'

    return render_template('signup.html.j2', log=msg)


@web_app.route('/sign_up_two', methods =['GET','POST'])
def sign_up_two():
    print(session['profileimg'])
    if request.method == 'POST' and request.form['phonenumber'] and request.form['nationalId']\
        and request.form['bio'] and request.files['nationalidimg'] and request.files['nationalidimg'].filename != '':

        # save session data
        for entry, value in request.form.to_dict().items():
            session[entry] = value

        
        url = ImageProcessing.upload_img(request.files['nationalidimg'])
        session['nationalidimg'] = url

        if session['usertype'] == 'student':
            return redirect(url_for('sign_up_student'))
        else:
            return redirect(url_for('sign_up_host'))
    return render_template('signup2.html.j2')


@web_app.route('/sign_up_student', methods =['GET','POST'])
def sign_up_student():
    message = ''
    if request.method == 'POST' and 'studentidimg' in request.files\
          and request.files['studentidimg'].filename != '' and 'referenceimg' in request.files\
          and request.files['referenceimg'].filename != '' and "emergencycontact" in request.form:
        
        session['studentidimg'] = ImageProcessing.upload_img(request.files['studentidimg'])
        session['referenceimg'] = ImageProcessing.upload_img(request.files['referenceimg'])
        session['emergencycontact'] = request.form['emergencycontact']

        user_data = {}
        email = session['email']
        password = session['password']
        for record_key, record_value in session.items():

            if record_key == 'password':
                continue
            user_data[record_key] = record_value

        response = Students.add_student(user_data)

        images = SessionProcessing.clear_session(session)
        print(response)
        if response == 200:
            create_user_response = Authentication.signup(email, password)
            session.clear()
            if create_user_response == 200:
                message = 'Account created successfully'
                return redirect(url_for('login', msg=message))
        
        SessionProcessing.clear_session_images(images)
        message = 'Sorry, Failed to create account'
        return redirect(url_for('sign_up_one', msg=message))

    return render_template('signup3.html.j2')


@web_app.route('/sign_up_host', methods =['GET','POST'])
def sign_up_host():
    
    if request.method == 'POST' and request.form['nokfullname'] and request.form['noknumber']\
          and request.form['nokaddress']:
        
        session['nextofkin'] = {'name': request.form['nokfullname'], 'number': request.form['noknumber'], 'address': request.form['nokaddress']}

        user_data = {}
        for record_key, record_value in session.items():
            if record_key == 'password':
                continue
            user_data[record_key] = record_value
        
        response = Hosts.add_host(user_data)

        images = SessionProcessing.clear_session(session)
        
        if response == 200:
            create_user_response = Authentication.signup(session['email'], session['password'])
            session.clear()
            if create_user_response == 200:
                message = 'Account created successfully'
                return redirect(url_for('login', msg=message))
            
        SessionProcessing.clear_session_images(images)
        message = 'Sorry, Failed to create account'
        return redirect(url_for('sign_up_one', msg=message))

    return render_template('signup4.html.j2')

@web_app.route('/end_process', methods =['GET','POST'])
def end_process():

    images = SessionProcessing.clear_session(session)
    SessionProcessing.clear_session_images(images)
    

    return redirect(url_for('index', msg="Sign up cancelled"))
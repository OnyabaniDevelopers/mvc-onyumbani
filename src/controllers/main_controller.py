from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing

from src.models.FirebaseAuth import Authentication
from src.models.Students import Students
from src.models.Hosts import Hosts

@web_app.route('/upload', methods=['POST'])
def upload():

    # getting image from the request
    image = request.files['image']
    
    filename, url = ImageProcessing.upload_img(image)
    
    print(url)
    
    return redirect(url_for('index'))


# clear session of closing browser
@socketio.on('disconnect')
def clear_session():
    session.pop('loggedin', None)


#route index
@web_app.route('/')
def index():
    '''Index page controller'''

    # change tab value for logout/login
    login_or_logout_tab = {'value':'Log in / Sign up'}
    if session.get('loggedin') == True:
        login_or_logout_tab = {'value': 'Log out'}

    return render_template('index.html.j2', data=login_or_logout_tab)
    # return render_template('image_upload.html.j2')
    
  

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

'''
Signing in process
'''
    
@web_app.route('/sign_up_one', methods =['GET', 'POST'])
def sign_up_one():
    if request.method == 'POST' and 'password' in request.form and 'confirmpassword' in request.form\
        and 'lastname' in request.form and 'firstname' in request.form and 'homeaddress' in request.form\
            and 'dob' in request.form and 'usertype' in request.form and 'email' in request.form\
                and request.form['password'] == request.form['confirmpassword']:
        # save session data
        
        session['lastname'] = request.form['lastname']
        session['firstname'] = request.form['firstname']
        session['usertype'] = request.form['usertype']
        session['dob'] = request.form['dob']
        session['password'] = request.form['password']
        session['email'] = request.form['email']
        session['homeaddress'] = request.form['homeaddress']

        if 'profileimage' in request.files and request.files['profileimage'].filename != '':
            url = ImageProcessing.upload_img(request.files['profileimage'])
            session['profileimg'] = url

            
        return redirect(url_for('sign_up_two'))

    return render_template('signup.html.j2')


@web_app.route('/sign_up_two', methods =['GET','POST'])
def sign_up_two():
    print(session['profileimageurl'])
    if request.method == 'POST' and 'phonenumber' in request.form and 'idnumber' in request.form\
        and 'bio' in request.form and 'nationalidimg' in request.files and request.files['nationalidimg'].filename != '':

        print(session['email'])
        # save session data
        session['phonenumber'] = request.form['phonenumber']
        session['nationalId'] = request.form['idnumber']
        session['bio'] = request.form['bio']

        
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

        SessionProcessing.clear_session(session)

        if response == 200:
            create_user_response = Authentication.signup(email, password)
            session.clear()
            if create_user_response == 200:
                message = 'Account created successfully'
                return redirect(url_for('login', msg=message))
        
        message = 'Sorry, Failed to create account'
        return redirect(url_for('sign_up_one', msg=message))

    return render_template('signup3.html.j2')


@web_app.route('/sign_up_host', methods =['GET','POST'])
def sign_up_host():
    
    if request.method == 'POST' and 'nokfullname' in request.form and 'noknumber' in request.form\
          and 'nokaddress' in request.form:
        
        session['nextofkin'] = {'name': request.form['nokfullname'], 'number': request.form['noknumber'], 'address': request.form['nokaddress']}

        user_data = {}
        for record_key, record_value in session.items():
            if record_key == 'password':
                continue
            user_data[record_key] = record_value
        
        response = Hosts.add_host(user_data)

        SessionProcessing.clear_session(session)
        
        if response == 200:
            create_user_response = Authentication.signup(session['email'], session['password'])
            session.clear()
            if create_user_response == 200:
                message = 'Account created successfully'
                return redirect(url_for('login', msg=message))
        
        message = 'Sorry, Failed to create account'
        return redirect(url_for('sign_up_one', msg=message))

    return render_template('signup4.html.j2')

@web_app.route('/sign_up_host', methods =['GET','POST'])
def end_signup():

    SessionProcessing.clear_session(session)

    return redirect(url_for('index', msg="Sign up cancelled"))

    




from datetime import date, timedelta, datetime
import time
from src import web_app, socketio
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import check_availability, get_dates_between
from src.models.Reviews import Reviews
from src.models.Students import Students
from src.utils.email_notification_processing import EmailNotifier
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
    
    msg = ''
    color = ''

    # change tab value for logout/login
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
        
    
    all_homes = Homes.get_homes()
    
    if 'msg' in request.args:
        msg = request.args.get('msg')
        color = request.args.get('color')

    amenities = []
    for entry, value in request.args.to_dict().items():
            if 'amenity' in entry and value:
                amenities.append(value)
                
    if ('location' in request.args and request.args['location'])\
          or ('maxprice' in request.args and request.args['maxprice'])\
          or ('startdate' in request.args and request.args['startdate'])\
              or ('enddate' in request.args and request.args['enddate'])\
                or len(amenities) != 0:
        
        filtered_homes = {}
        for home_key, home in all_homes.items():

            #check amenities
            if len(amenities):
                if check_availability(amenities, home['amenities']):
                    filtered_homes[home_key] = home

            #check location filter
            if request.args['location'] and home['city'] == request.args['location']:
                filtered_homes[home_key] = home

            # check price filter
            if request.args['maxprice'] and int(request.args['maxprice']) >= int(home['roomprice']):
                filtered_homes[home_key] = home
            
            # check availability filter 
            if request.args['startdate'] and request.args['enddate']: 
                available_dates = get_dates_between(home['initdate'], home['enddate'])
                required_dates = get_dates_between(request.args['startdate'], request.args['enddate'])
                if check_availability(required_dates, available_dates):
                    filtered_homes[home_key] = home
            
        return render_template('index.html.j2', msg=msg, color=color, data=data, homes=filtered_homes)

    return render_template('index.html.j2', msg=msg, color=color, data=data, homes=all_homes)

@web_app.route('/view_profile')
def view_profile():
    log = ' '
    color = ' '
    
    profile_data = {}
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
        userId = session['userId']
        if session['usertype'] == 'owner':
           profile_data = Hosts.get_host(userId)  
           
        else:
             profile_data = Students.get_student(userId) 
             
        if 'profileimg' not in profile_data:
                profile_data['profileimg'] = url_for('static', filename='pics/profile.png')
                
        if 'log' in request.args:
            log = request.args.get('log')
            color = request.args.get('color')
    
        return render_template('viewprofile.html.j2', data=data, profile_data=profile_data, log=log, color=color)
     
    msg = "Please Log in first"
    return redirect(url_for('login', msg=msg))

# endpoint to view otheer users profile e.g student viewing owner or owner viewing student
@web_app.route('/view_profile/<usertype>/<userId>')
def view_profile_all(userId, usertype):

    profile_data = {}
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']

    if usertype == 'owner':
        profile_data = Hosts.get_host(userId)  
    else:
        profile_data = Students.get_student(userId) 
        
    if 'profileimg' not in profile_data:
        profile_data['profileimg'] = url_for('static', filename='pics/profile.png')
    
    return render_template('viewprofile2.html.j2', data=data, profile_data=profile_data)


@web_app.route('/about', methods=['GET', 'POST'])
def about():
    '''About page controller'''
    msg=" "

    # change tab value for logout/login
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
    
        # all_homes = Homes.get_homes()

        if request.method == 'POST' and request.form['senderemail'] and request.form['sendername']\
        and request.form['message']:
            message =  f"Your message: \t{request.form['message']} \n\nThank you for your message, customer service will get back to you soon"
            EmailNotifier.send_email(request.form['senderemail'], message, request.form['sendername'])
            msg="Message was sent successfully"
            
            return render_template('about.html.j2', data=data, color='green', about_msg=msg)
            
        if request.method == 'POST':
            msg="*Sorry, some required information are missing"
            
    elif request.method == 'POST':
        msg = "Please Log in first"
    
    return render_template('about.html.j2', data=data, color='green', about_msg=msg)
        

    
@web_app.route('/updateprofile', methods =['GET','POST'])
def updateprofile():
    msg=''
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
                response = Hosts.delete_host(session['userId'], session['email'])
            elif session['usertype'] == 'student':
                response = Students.delete_student(session['userId'], session['email'])
                
            if response == 200:
                msg='Delete successful'
                return redirect(url_for('login', log=msg))
         
        msg='Failed to delete'
        return redirect(url_for('view_profile', log=msg, color='#FF3062'))
        
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
    

@web_app.route('/review/<type>/<id>', methods =['POST'])
def review(type, id):

    if request.method == 'POST' and request.form['rating'] and request.form['reviewmessage']:

        review_data = {}
        review_data['dateposted'] = str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
        review_data['rating'] = int(request.form['rating'])
        review_data['reviewmessage'] = request.form['reviewmessage']
        review_data['email'] = session['email']
        review_data['image'] = ''

        response = Reviews.add_review(id, type, review_data)

        if response[1] == 200:

            if type == 'home':

                return redirect(url_for('view_home', id=id))
            #TODO: add else for student review (only for home owners)
    return redirect(url_for('view_home', id=id, errors='Failed to add comment'))       
    

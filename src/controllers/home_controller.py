import time
from src import web_app
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import encrypt_num, get_dates_between, get_geocode
from src.models.Hosts import Hosts
from src.models.Reviews import Reviews
from src.models.Students import Students
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing


from src.models.Homes import Homes

@web_app.route('/view_listed', methods =['GET', 'POST'])
def view_listed():

    msg = ''
    color = ''
    all_homes = Homes.get_homes()
    user_applications = {}

    user_homes = {}

    
    # change tab value for logout/login
    tabs = {'log_status':'Sign In / Up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}
        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else 'Applications'

        for home_key, home  in all_homes.items():
            if home['userId'] == session['userId']:
                user_homes[home_key] = home

        applications = Students.get_applications('owner', session['userId'])

        for application in applications:
            user_applications[application['appId']] = application
        
        if request.method == 'GET' and 'change' in request.args and 'id' in request.args:
            print(request.args['change'])
            appId = request.args['id']
            if request.args['change'] == 'disapprove':
                Hosts.update_application({'status':'disapproved'}, appId)
            elif request.args['change'] == 'approve':
                Hosts.update_application({'status':'Make payment'}, appId)

            applications = Students.get_applications('owner', session['userId'])

            for application in applications:
                user_applications[application['appId']] = application

            return render_template('homesapplicationview.html.j2', data=tabs, homes=user_homes, applications=user_applications)


    

    return render_template('homesapplicationview.html.j2', data=tabs, homes=user_homes, applications=user_applications)


@web_app.route('/add_home', methods =['GET', 'POST'])
def add_home():
    msg=' '
    if request.method == 'POST' and request.form['homename'] and request.form['homeaddress']\
        and request.form['homedescription'] and request.files['ownershipimg']\
                    and request.form['city'] and request.form['country']\
                    and request.form['initdate'] and request.form['enddate']:
        
        session['homeId'] = f"{int(time.time() * 1000)}"
        session['amenities'] = []
        for entry, value in request.form.to_dict().items():
            if 'amenity' in entry:
                refined_entry = entry.split('-')[-1]
                session['amenities'].append(refined_entry)
                continue
            session[entry] = value
        session['ownershipimg'] = ImageProcessing.upload_img(request.files['ownershipimg'])

        return redirect(url_for('add_room'))
    
    elif request.method == 'POST':
        SessionProcessing.clear_session_images(SessionProcessing.clear_session(session))
        msg = "*Sorry, some required fields are missing, re-enter information"
    return render_template('addhome.html.j2', error_message=msg)


@web_app.route('/add_room', methods =['GET', 'POST'])
def add_room():
    msg=' '
    if request.method == 'POST' and request.form['numpeople'] and request.form['roomprice']\
        and request.files['homeimgs'] and request.form['numrooms']\
            and request.form['roomdescription']:

        for entry, value in request.form.to_dict().items():
            session[entry] = value 
        
        session['homeimgs'] = []
        
        for image in request.files.getlist('homeimgs'):
            img_url = ImageProcessing.upload_img(image)
            session['homeimgs'].append(img_url)

        home_data = {}
        for record_key, record_value in session.items():

            if record_key in ['loggedin', 'usertype', '_permanent']:
                continue

            home_data[record_key] = record_value

        response = Homes.add_home(home_data)

        images = SessionProcessing.clear_session(session)

        if response == 200:
            message = 'Home added successfully'
            return redirect(url_for('view_listed', error_message=msg))
        else:
            SessionProcessing.clear_session_images(images)
    elif request.method == 'POST':
        msg = '*Sorry, some required information are missing'
        
    return render_template('addroom.html.j2', error_message=msg)

@web_app.route('/view_home/<id>', methods =['GET', 'POST'])
def view_home(id):
    # session['currentpage'] = url_for('view_home', id=id)
    
    msg=''
    
    if 'errors' in request.args:
        msg = request.args['errors']
    
    if 'error_messages' in session:
        msg = session['error_messages']

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
      
    home_data = Homes.get_home(id)
    home_data['numrooms'] = int(home_data['numrooms'])

    # encrypt prize before adding data
    encrypt_price = encrypt_num(home_data['roomprice'])
    home_data['encryptprice'] = encrypt_price

    host_data = Hosts.get_host(home_data['userId'])
    
    if 'profileimageurl' not in host_data:
        host_data['profileimageurl'] = url_for('static', filename='pics/profile.png')

    # get dates list
    dates_list = get_dates_between(home_data['initdate'], home_data['enddate'])
    home_data['dateslist'] = dates_list

    # get latitude and longitude for location
    full_address = f"{home_data['homeaddress']}, {home_data['city']}, {home_data['country']}"
    city_country = f"{home_data['city']}, {home_data['country']}"
    location = get_geocode(full_address)
    if location == None:
        location = get_geocode(city_country)

    
    #load reviews
    response = Reviews.get_reviews(id, 'home')
 
    reviews = response[0] if response[1] == 200 else []

    return render_template('individualhome.html.j2', home_data=home_data, reviews=reviews, data=tabs, host_data=host_data, location=location, errors=msg)


@web_app.route('/edithome', methods =['GET', 'POST'])
def edithome():
    msg="  "

    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    applications=[]
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else "Applications"
        
        if request.method == 'POST' and request.form['paymentname'] and request.form['mode']\
            and request.form['transaction']  and request.form['amount'] and request.files['paymentimg']:
            pass
            
        elif request.method == 'POST':
            msg = "*Sorry, some required fields are missing, re-enter information"
            
        return render_template('edithome.html.j2', data=tabs, msg=msg)  
        
    else:
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
    
@web_app.route('/delete_home/<homeId>/<ownerId>', methods =['GET'])
def delete_home(homeId, ownerId):
    msg = ' '
    
    if 'loggedin' in session and session['loggedin'] == True:
            
            applications = Students.get_applications('owner', ownerId)

            response = Homes.delete_home(homeId)
                
            if response == 200:
                msg='Delete successful'
                for application in applications:
                    if application['homeId'] == homeId:
                        Students.delete_application(application['appId'])
                return redirect(url_for('view_listed', log=msg))
         
            msg='Failed to delete'
            return redirect(url_for('view_listed', log=msg, color='#FF3062'))
        
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
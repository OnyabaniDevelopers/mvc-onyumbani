import time
from src import web_app
from flask import render_template, redirect, url_for, request, session
from src.models.Hosts import Hosts
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing


from src.models.Homes import Homes


@web_app.route('/add_home', methods =['GET', 'POST'])
def add_home():
    msg=''
    if request.method == 'POST' and request.form['homename'] and request.form['homeaddress']\
        and request.form['homedescription'] and request.files['ownershipimg']\
                    and request.form['city'] and request.form['country']:
        
        session['homeId'] = f"{int(time.time() * 1000)}"
        session['amenities'] = {}
        for entry, value in request.form.to_dict().items():
            if 'amenity' in entry:
                refined_entry = entry.split('-')[-1]
                session['amenities'][entry] = refined_entry
                continue
            session[entry] = value
            

        session['ownershipimg'] = ImageProcessing.upload_img(request.files['ownershipimg'])

        return redirect(url_for('add_room'))
    else:
        SessionProcessing.clear_session_images(SessionProcessing.clear_session(session))
        msg = "Sorry, we are missing some required fields, re-enter again"
    return render_template('addhome.html.j2', error_message=msg)


@web_app.route('/add_room', methods =['GET', 'POST'])
def add_room():
    msg=''
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

            if record_key in ['loggedin', 'usertype']:
                continue

            home_data[record_key] = record_value

        response = Homes.add_home(home_data)
        print(response)

        images = SessionProcessing.clear_session(session)

        if response == 200:
            print('we are here')
            message = 'Home added successfully'
            return redirect(url_for('index', msg=message))
        else:
            print(response)
            SessionProcessing.clear_session_images(images)
    message = 'Sorry, Failed to add home'
    return render_template('addroom.html.j2', msg=message)

@web_app.route('/view_home/<id>', methods =['GET', 'POST'])
def view_room(id):
    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
      
    home_data = Homes.get_home(id)
    host_data = Hosts.get_host(home_data['userId'])  
    return render_template('individualhome.html.j2', home_data=home_data, data=tabs, host_data=host_data)

@web_app.route('/reserve')
def reserve_room():

    if 'loggedin' not in session or session['loggedin'] == False:
         
         msg = "Please Log in first"
         return redirect(url_for('login', msg=msg))



    return render_template('payment.html.j2')
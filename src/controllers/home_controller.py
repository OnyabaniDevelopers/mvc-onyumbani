import time
import codecs
from src import web_app
from flask import jsonify, render_template, redirect, url_for, request, session
from src.models.Hosts import Hosts
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing


from src.models.Homes import Homes



def encrypt_num(num):
    num_alpha = {'1':'y', '2':'x', '3':'w', '4':'v', '5':'u', '6':'t', '7':'s', '8':'r', '9':'q', '0':'a'}
    num_str = ''
    for digit in num:
        num_str += num_alpha[digit]

    return codecs.encode(num_str, 'rot_13')

def decrypt_num(enc_str):
    alpha_num = {'y':'1', 'x':'2', 'w':'3', 'v':'4', 'u':'5', 't':'6', 's':'7', 'r':'8', 'q':'9', 'a':'0'}
    num_str = codecs.decode(enc_str, 'rot_13')
    num = ''

    for letter in num_str:
        num += alpha_num[letter]
    
    return num





@web_app.route('/add_home', methods =['GET', 'POST'])
def add_home():
    msg=' '
    if request.method == 'POST' and request.form['homename'] and request.form['homeaddress']\
        and request.form['homedescription'] and request.files['ownershipimg']\
                    and request.form['city'] and request.form['country']\
                    and request.form['initdate'] and request.form['enddate']:
        
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

            if record_key in ['loggedin', 'usertype']:
                continue

            home_data[record_key] = record_value

        response = Homes.add_home(home_data)

        images = SessionProcessing.clear_session(session)

        if response == 200:
            message = 'Home added successfully'
            return redirect(url_for('index', error_message=msg))
        else:
            SessionProcessing.clear_session_images(images)
    elif request.method == 'POST':
        msg = '*Sorry, some required information are missing'
        
    return render_template('addroom.html.j2', error_message=msg)

@web_app.route('/view_home/<id>', methods =['GET', 'POST'])
def view_room(id):
    session['currentpage'] = f'/view_room/{id}'
    # change tab value for logout/login
    tabs = {'log_status':'Log in / Sign up', 'add_home':''}
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
      
    home_data = Homes.get_home(id)
    encrypt_price = encrypt_num(home_data['roomprice'])
    home_data['encryptprice'] = encrypt_price
    host_data = Hosts.get_host(home_data['userId'])  
    return render_template('individualhome.html.j2', home_data=home_data, data=tabs, host_data=host_data)
    
@web_app.route('/reserve/<id>/<price>')
def reserve_room(id, price):
    session['currentpage'] = f'/reserve/{id}/{price}'
    if 'loggedin' in session and session['loggedin'] == True:
        tabs = {'log_status': 'Log out'}

        tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', msg=msg))

    new_price = decrypt_num(price)

    return render_template('reservation.html.j2', data=tabs, price=new_price)

# @web_app.route('/reserve/<id>/<price>')
# def reserve_room(id, price):
#     session['currentpage'] = f'/reserve/{id}/{price}'
#     if 'loggedin' in session and session['loggedin'] == True:
#         tabs = {'log_status': 'Log out'}

#         tabs['add_home'] = 'Add Home' if session['usertype'] == 'owner' else ""
    
#     else:      
#         msg = "Please Log in first"
#         return redirect(url_for('login', msg=msg))

#     new_price = decrypt_num(price)

#     return render_template('payment.html.j2', data=tabs, price=new_price)


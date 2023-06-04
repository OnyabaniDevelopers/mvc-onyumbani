from src import web_app
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import check_availability, decrypt_num, get_dates_between
from src.models.Homes import Homes
from src.models.Hosts import Hosts
from src.models.Students import Students
from datetime import datetime, date
from src.utils.email_notification_processing import EmailNotifier


@web_app.route('/adminview', methods =['GET', 'POST'])
def adminview():
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
            
        return render_template('adminapplication.html.j2', data=tabs, msg=msg)  
        
    else:
        msg = "Please login as admin first"
        return redirect(url_for('login', msg=msg))
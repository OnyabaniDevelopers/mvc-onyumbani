from src import web_app
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import check_availability, decrypt_num, get_dates_between
from src.models.Homes import Homes
from src.models.Hosts import Hosts
from src.models.Payments import Payments
from src.models.Students import Students
from datetime import datetime, date
from src.utils.email_notification_processing import EmailNotifier


@web_app.route('/adminview', methods =['GET', 'POST'])
def adminview():
    msg="  "

    # change tab value for logout/login
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
        
        payments = Payments.get_payments()[0]
        updated_payments = {}
        for paymentid, payment in payments.items():
            
            application_data = Students.get_application(payment['applicationid'])
            if application_data[1] == 200:
                payment['application'] = application_data[0]
            updated_payments[paymentid] = payment
 
        return render_template('adminapplication.html.j2', data=data, msg=msg, payments=updated_payments)  
        
    else:
        msg = "Please login as admin first"
        return redirect(url_for('login', log=msg))
    
@web_app.route('/cancel_payment/<appId>/<paymentId>', methods =['GET'])
def cancel_payment(appId, paymentId):
    msg = ' '
    
    if 'loggedin' in session and session['loggedin'] == True:

        response = Payments.delete_payment(paymentId)
                
        if response[1] == 200:
            Hosts.update_application({'status':'Payment declined'}, appId)
            msg='Payment cancelled successful'
            return redirect(url_for('adminview', log=msg))
         
        msg='Failed to cancel payment, try later'
        return redirect(url_for('adminview', log=msg, color='#FF3062'))
        
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))

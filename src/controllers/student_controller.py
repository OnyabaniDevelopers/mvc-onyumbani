
from src import web_app
from flask import render_template, redirect, url_for, request, session
from src.controllers.helper_functions import check_availability, decrypt_num, get_dates_between
from src.models.Homes import Homes
from src.models.Hosts import Hosts
from src.models.Payments import Payments
from src.models.Students import Students
from datetime import datetime, date
from src.utils.email_notification_processing import EmailNotifier
from src.utils.image_processing import ImageProcessing
from src.utils.session_processing import SessionProcessing

@web_app.route('/reserve/<homeid>/<price>', methods =['GET', 'POST'])
def reserve_room(homeid, price):

    
    error_messages = ''
    errors = ''
    session['currentpage'] = f'/reserve/{homeid}/{price}'

    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
    
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', msg=msg))
    new_price = decrypt_num(price)

    home_data = Homes.get_home(homeid)
    if request.method == 'POST' and request.form['numrooms'] and request.form['checkin']\
        and request.form['checkout'] and request.files['schoolrefimg']:
        
        # check number of rooms
        num_rooms = request.form['numrooms']
        if int(home_data['numrooms']) < int(request.form['numrooms']):
            error_messages = "Required number of rooms is not available\n"

        # confirm dates
        checkin_date = datetime.strptime(request.form['checkin'], '%Y-%m-%d').date()
        checkout_date = datetime.strptime(request.form['checkout'], '%Y-%m-%d').date()
        
        if checkout_date < checkin_date:
            error_messages = "Check in date and check out date are inconsistent\n"

        available_dates = home_data['dateslist']
        required_dates = get_dates_between(request.form['checkin'], request.form['checkout'])
        if not check_availability(required_dates, available_dates):
            error_messages = "The time period you want to stay is not available"
        
        if not error_messages:
            session['schoolrefimg'] = ImageProcessing.upload_img(request.files['schoolrefimg'])
            session['ownerId'] = home_data['userId']
            dates = [request.form['checkin'], request.form['checkout']]
            homename = home_data['homename']
            return render_template('reservation.html.j2', data=data, homeId=homeid, homename=homename, num_rooms=num_rooms, dates=dates, price=new_price)
        else:
            SessionProcessing.clear_session_images(SessionProcessing.clear_session(session))
            
    return redirect(url_for('view_home', id=homeid, errors=error_messages))


@web_app.route('/apply/<id_room_dates_name>', methods=['POST', 'GET'])
def apply_housing(id_room_dates_name):

    args_list = id_room_dates_name.split('aq')
    homeId = args_list[0]
    num_rooms = args_list[1]
    init_date = args_list[2]
    end_date = args_list[3]
    price = args_list[4]
    homename = args_list[5]


    host_data = Hosts.get_host(session['ownerId'])

    profile_data = Students.get_student(session['userId'])

    num_days = len(get_dates_between(init_date, end_date))
    stay_price = round((int(price)/30)*num_days, 2)

    application_data = {}

    application_data['Prefer-students'] = request.form['buddy']
    application_data['School-Reference'] = session['schoolrefimg']
    application_data['homeId'] = homeId
    application_data['ownerId'] = session['ownerId']
    application_data['application-date'] = str(date.today())
    application_data['studentId'] = session['userId']
    application_data['guests'] = {}
    application_data['applicant_email'] = session['email']
    application_data['owner_email'] = host_data['email']
    application_data['status'] = 'Host approval'
    application_data['numrooms'] = num_rooms
    application_data['initdate'] = init_date
    application_data['enddate'] = end_date
    application_data['roomprice'] = stay_price
    application_data['studentname'] = f"{profile_data['firstname']} {profile_data['firstname']}"
    application_data['studentcontact'] = profile_data['phonenumber']
    application_data['homename'] = homename

    guests_emails = []
    if request.form['guests'] != '0':
        num_guests = request.form['guests']
        for i in range(int(num_guests)):
            i = i+1
            fullname = request.form[f"fullname{i}"]
            idnum = request.form[f"idnum{i}"]
            email = request.form[f"email{i}"]
            application_data['guests'][i] = [fullname, idnum, email]
            guests_emails.append(email)

    response = Students.submit_application(application_data)

    if guests_emails:
        message = f"{session['email']}, entered you as guests. Please follow this link to confirm"
        EmailNotifier.send_email(guests_emails, message, ' ')

    SessionProcessing.clear_session_images(SessionProcessing.clear_session(session))

    if response == 200:

        return redirect(url_for('view_application'))
    
    else:
        return redirect(f'/view_home/{homeId}')
        
@web_app.route('/view_application', methods =['GET', 'POST'])
def view_application():
    msg=""

    # change tab value for logout/login
    applications=[]
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
        
        applications = Students.get_applications('student', session['userId'])
    
    all_homes = Homes.get_homes()

    status = []
    updated_applications = []
    if applications != []:
        
        for application in applications:
            home = all_homes[application['homeId']]
            room_taken_info = ""

            if int(home['numrooms']) < int(application['numrooms']):
                room_taken_info += "The room(s) required are not available<br>"
            
            available_dates = home['dateslist']
            required_dates = get_dates_between(application['initdate'], application['enddate'])
            if not check_availability(required_dates, available_dates):
                room_taken_info += "The time period you want to stay is not available<br>" 

            
            if room_taken_info:
                msg = room_taken_info
                Hosts.update_application({'status':'closed'}, application['appId'])
                application['status'] = 'closed'
                application['states'] = []
            
            else:
                msg = " "
                application['states'] = ['Host approval', 'Make payment', 'Payment received', 'Ready to go']
            
            updated_applications.append(application)


    
    return render_template('applications.html.j2', data=data, homes=all_homes, msg=msg, applications=updated_applications)  
    
@web_app.route('/make_payment/<homeId>/<appId>/<roomprice>', methods =['GET', 'POST'])
def make_payment(roomprice, homeId, appId):
    msg=""
    
    # change tab value for logout/login
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
 

    return render_template('payment.html.j2',  data=data, price=roomprice, homeId=homeId, appId=appId)
    
        
    
@web_app.route('/confirmpayment/<homeId>/<appId>', methods =['GET', 'POST'])
def confirmpayment(homeId, appId):
    msg="   "

    # change tab value for logout/login
    
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}

        data['usertype'] = session['usertype']
        
        if request.method == 'POST' and request.form['paymentname'] and request.form['mode']\
            and request.form['transaction']  and request.form['amount'] and request.files['paymentimg']:
            profile_data = Students.get_student(session['userId'])

            payment_data = {}
            for entry, value in request.form.to_dict().items():
                payment_data[entry] = value

            payment_data['date'] = str(date.today())
            payment_data['paymentimg'] = ImageProcessing.upload_img(request.files['paymentimg'])
            payment_data['studentid'] = session['userId']
            payment_data['homeid'] = homeId
            payment_data['applicationid'] = appId

            response = Payments.make_payment(payment_data)

            if response[1] == 200:
                msg="Payment details submitted successfully"
                Hosts.update_application({'status':'Payment received'}, appId)

            else:
                msg="Payment details submission was not successful"

            return redirect(url_for('view_application'))

            
        elif request.method == 'POST':
            msg = "*Sorry, some required fields are missing, re-enter information"
            
        return render_template('payment1.html.j2', data=data, msg=msg, homeId=homeId, appId=appId)  
        
    else:
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
    
@web_app.route('/delete_application/<appId>', methods =['GET'])
def delete_application(appId):
    msg = ' '
    
    if 'loggedin' in session and session['loggedin'] == True:

        response = Students.delete_application(appId)
                
        if response[1] == 200:
            msg='Application cancelled successful'
            return redirect(url_for('view_application', log=msg))
         
        msg='Failed to cancel application, try later'
        return redirect(url_for('view_application', log=msg, color='#FF3062'))
        
    else:      
        msg = "Please Log in first"
        return redirect(url_for('login', log=msg))
  

import codecs
import smtplib
import geocoder
from datetime import datetime, timedelta
from src import API_KEY, EMAIL, PASSWORD
import re

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

def get_geocode(address):
    
    g = geocoder.google(address, method='places', key=API_KEY)
    code = g.latlng
    return code


def get_dates_between(start_date, end_date):
    print("started")
    dates_list = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    print(current_date, end_date)

    while current_date <= end_date:
        dates_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return dates_list
 
 
def check_availability(A, B):
  # convert list A to string
    A_str = ' '.join(map(str, A))
    # convert list B to string
    B_str = ' '.join(map(str, B))
    # find all instances of A within B
    instances = re.findall(A_str, B_str)
 
    # return True if any instances were found, False otherwise
    return len(instances) > 0


def send_email(sender_email, message, sender_name):       
    # Set up the SMTP server details
    from_email = EMAIL
    password = PASSWORD
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection: 
        email_password = password
        connection.login(from_email, email_password )
        connection.sendmail(from_addr=from_email, to_addrs=sender_email, 
        msg=f"subject:Onyumbani Web Message \n\n Hi, {sender_name}\n\nYour message: \t{message} \n\nThank you for your message, customer service will get back to you soon\n\n Kind regards, \n\n Onyumbani Team")
 
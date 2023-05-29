import codecs
import geocoder
from datetime import datetime, timedelta
from src import API_KEY

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
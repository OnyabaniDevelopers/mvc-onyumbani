import json
import urllib3
from src import API_KEY
import firebase_admin
from firebase_admin import auth
from src.models.constants import BASE_URL
from src.utils.email_notification_processing import EmailNotifier
request_ref = BASE_URL + '/userinfo'


#TODO: Hide all sensitive data like APIKEY

class Authentication:

    def __init__(self):
        pass
    
    @staticmethod
    def login(email, password):
        request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={0}".format(API_KEY)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object
    
    @staticmethod
    def signup(email, password):
        try:
            request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={0}".format(API_KEY)
            headers = {"content-type": "application/json; charset=UTF-8"}
            data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
            request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
                  
            return request_object.status
        except:
            return 404

    @staticmethod
    def get_user_info(email):
        try:
            headers = {"content-type": "application/json; charset=UTF-8"}
            request_object = urllib3.request(method="GET",url=request_ref+f"/{email}", headers=headers)
            return eval(request_object.data.decode())
        except:
            return 404

    @staticmethod
    def delete_user(uid):
        try:
            request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:delete?key={0}".format(API_KEY)
            headers = {"content-type": "application/json; charset=UTF-8"}
            data = json.dumps({"returnSecureToken": True, "idToken":uid})
            request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
                  
            return request_object.status
        except:
            return 404
        
    @staticmethod
    def send_email_verification(email, name):
        link = auth.generate_email_verification_link(email, action_code_settings=None, app=None)
        print(link)
        message = f'Welcome to O~nyumbani Housing\n\nPlease copy the link below to your browser to verify your account\n{link}'
        EmailNotifier.send_email(email, message, name)

    @staticmethod
    def is_verified(email):
        data = auth.get_user_by_email(email, app=None)
        return data.email_verified
   
            
    
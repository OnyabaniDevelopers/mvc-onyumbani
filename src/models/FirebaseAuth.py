import json
import urllib3


#TODO: Hide all sensitive data like APIKEY

class Authentication:

    def __init__(self):
        pass
    
    @staticmethod
    def login(email, password):
        request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={0}".format('AIzaSyBOx2Perl8ixzncFwkjV5SdDgFDI12xUqY')
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object
    
    @staticmethod
    def signup(email, password):
        print('started')
        try:
            request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={0}".format('AIzaSyBOx2Perl8ixzncFwkjV5SdDgFDI12xUqY')
            headers = {"content-type": "application/json; charset=UTF-8"}
            data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
            request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
            print("status", request_object.status)        
            return request_object.status
        except:
            print("failed")
            
    
from flask import jsonify
import urllib3
from src.models.constants import BASE_URL
import json
from src import database

application_db = database.collection('applications')

request_ref = BASE_URL + '/students'
application_ref = BASE_URL + '/applications'

class Students:

    def __init__():
        pass

    @staticmethod
    def add_student(sign_up_data):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(sign_up_data)
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object.status
        
    @staticmethod
    def update_student(sign_up_data, student_id):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(sign_up_data)
        request_object = urllib3.request(method="PUT",url=request_ref+f'/{student_id}', headers=headers, body=data)
        return request_object.status
    
    @staticmethod
    def get_student(student_id):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="GET",url=request_ref+f'/{student_id}', headers=headers)
        return eval(request_object.data.decode())
        
    @staticmethod
    def delete_student(student_id, email):

        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="DELETE",url=request_ref+f'/{email}/{student_id}', headers=headers)
        return request_object.status
    
    @staticmethod
    def submit_application(application_data):
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(application_data)
        request_object = urllib3.request(method="POST",url=application_ref, headers=headers, body=data)
        return request_object.status
        
    @staticmethod
    def get_applications(usertype, userId):
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="GET",url=application_ref+f'/{usertype}/{userId}', headers=headers)
        return eval(request_object.data.decode())
    
    @staticmethod
    def delete_application(id):
        try:
            
            application_db.document(id).delete()
            response = {'SUCCESS': 'Deleted successfully'}
            return response, 200

        except:
            response = {"ERROR":"Unknown error"}
            return response, 503
        
    @staticmethod
    def get_application(appId):
        application = application_db.document(appId).get()

        if application:
            return application.to_dict(), 200

        return {"ERROR":"Unknown error"}, 404


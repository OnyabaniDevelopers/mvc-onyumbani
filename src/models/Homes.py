import  json
import urllib3
from src.models.constants import BASE_URL
import json
request_ref = BASE_URL + '/homes'
class Homes:

    def __init__():
        pass

    @staticmethod
    def add_home(sign_up_data):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(sign_up_data)
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object.status

    @staticmethod
    def get_homes():
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="GET",url=request_ref, headers=headers)
        return eval(request_object.data.decode())
    
    @staticmethod
    def get_home(home_id):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="GET",url=request_ref+f'/{home_id}', headers=headers)
        return eval(request_object.data.decode())
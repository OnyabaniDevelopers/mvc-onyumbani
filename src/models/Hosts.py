import urllib3
from src.models.constants import BASE_URL
import json
request_ref = BASE_URL + '/owners'
class Hosts:

    def __init__():
        pass

    @staticmethod
    def add_host(sign_up_data):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        sign_up_data["returnSecureToken"] = True
        data = json.dumps(sign_up_data)
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object.status

    @staticmethod
    def get_host(owner_id):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        request_object = urllib3.request(method="GET",url=request_ref+f'/{owner_id}', headers=headers)
        return eval(request_object.data.decode())
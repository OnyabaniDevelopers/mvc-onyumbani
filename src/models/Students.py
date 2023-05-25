import urllib3
from src.models.constants import BASE_URL
import json
request_ref = BASE_URL + '/students'
class Students:

    def __init__():
        pass

    @staticmethod
    def add_student(sign_up_data):
        
        headers = {"content-type": "application/json; charset=UTF-8"}
        sign_up_data["returnSecureToken"] = True
        data = json.dumps(sign_up_data)
        request_object = urllib3.request(method="POST",url=request_ref, headers=headers, body=data)
        return request_object.status

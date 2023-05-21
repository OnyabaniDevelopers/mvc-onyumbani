import  json
"""
Connections to Database

This can be empty if we use an API
"""
class Home:

    def __init__(self):
        pass
    
    @staticmethod
    def get_home():

        #TODO: Load this from the API or directly
        data = {
        "title": "Onymbani",
        "body": "This is the Home page"}
        return data
    
    #TODO: Add other methods here - add_home, delete_home
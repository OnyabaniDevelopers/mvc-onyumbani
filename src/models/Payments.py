from flask import jsonify
from src import database

payments_db = database.collection('payments')

class Payments:

    def __init__():
        pass

    @staticmethod
    def make_payment(data):

        try:
            payments_db.document().set(data)
            return jsonify({"SUCCESS":"Review Added"}),200
            
        except Exception as e:

            return {"ERROR":str(e)}, 503
    
    @staticmethod
    def get_payments():
        
        try:       
            payments = {data.id:data.to_dict() for data in payments_db.stream()}     

            return payments, 200
        
        except Exception as e:

            return {"ERROR":str(e)}, 503
        
    @staticmethod
    def delete_payment(id):
        try:
            
            payments_db.document(id).delete()
            response = {'SUCCESS': 'Deleted successfully'}
            return response, 200

        except:
            response = {"ERROR":"Unknown error"}
            return response, 503
        
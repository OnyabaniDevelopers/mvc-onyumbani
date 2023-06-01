from flask import jsonify
from src import database

home_reviews_db = database.collection('home-reviews')
student_reviews_db = database.collection('student-reviews')

class Reviews:

    def __init__():
        pass

    @staticmethod
    def add_review(id, review_for, data):

        db = home_reviews_db if review_for == 'home' else student_reviews_db
    
        try:

            reviews = db.stream()
            for review in reviews:
                if review.document().id == id:
                    db.document(id).collection('reviews').document().set(data, merge=True)
                    return jsonify({"SUCCESS":"Review Added"}),200
                
            db.document(id).collection('reviews').document().set(data)
            return jsonify({"SUCCESS":"Review Added"}),200
            
        except Exception as e:

            return {"ERROR":str(e)}, 503
    
    @staticmethod
    def get_reviews(id, reviews_for):
        
        db = database.collection(f'home-reviews/{id}/reviews') if reviews_for == 'home'\
              else database.collection(f'student-reviews/{id}/reviews')

        try:       
            reviews = [data.to_dict() for data in db.stream()]      

            return reviews, 200
        
        except Exception as e:

            return {"ERROR":str(e)}, 503
from src import bucket
import time

class ImageProcessing:

    def __init__():
        pass
    
    @staticmethod
    def upload_img(image):
        filename = f"img{int(time.time() * 1000)}"

        # saving the image to storage
        blob = bucket.blob(filename)
        blob.upload_from_file(image, content_type='image/png')

        # Getting the image url
        return blob.public_url
    
    @staticmethod
    def delete_img(filename):

        # Deleting image from storage
        blob = bucket.blob(filename)
        blob.delete()




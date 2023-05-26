
from src.utils.image_processing import ImageProcessing
from flask import render_template, redirect, url_for

class SessionProcessing:

    def __init__(self) -> None:
        pass
    

    @staticmethod
    def clear_session_images(images):
        for record_key, record_value in images.items():
            if record_key.endswith('img'):
                filename = record_value.split('/')[-1]
                ImageProcessing.delete_img(filename)
            if record_key.endswith('imgs'):
                for image_url in record_key:
                    filename = image_url.split('/')[-1]
                    ImageProcessing.delete_img(filename)

    @staticmethod
    def clear_session(session):
        session_values = []
        images = {}
        for record_key, record_value in session.items():
            if record_key.endswith('img') or record_key.endswith('imgs'):
                images[record_key] = record_value
            session_values.append(record_key)

        for record_key in session_values:
            if record_key in ['loggedin', 'userId', 'usertype']:
                continue
            session.pop(record_key)
        return images
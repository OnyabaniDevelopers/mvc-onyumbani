
from src.utils.image_processing import ImageProcessing
from flask import render_template, redirect, url_for

class SessionProcessing:

    def __init__(self) -> None:
        pass
    

    @staticmethod
    def clear_session(session):
        for record_key, record_value in session.items():
            if record_key.endswith('img'):
                filename = record_value.split('/')[-1]
                ImageProcessing.delete_img(filename)
            session.pop(record_key)
from flask import Flask, session
from flask_session import Session
import firebase_admin
import os
from firebase_admin import credentials, storage
from flask_socketio import SocketIO

web_app = Flask("src")
web_app.config["SESSION_PERMANENT"] = False
web_app.config["SESSION_TYPE"] = "filesystem"

Session(web_app)

web_app.config['SECRET_KEY'] = 'onyumbani'

socketio = SocketIO(web_app)

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "onyumbanihousing-1cc4d",
  "private_key_id": "13d3f19c46fce5d0564002d137741ad66e3bd282",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC5kvJNd3QoMyJM\nb83z2c1QFoAGGxTMXamiybLJSWh0grdpGlmr+4ch59f9i69DAoVc4WPz0/t+zMrv\npKdZgWfqIAG8w3L5BuKCVThRTO3lo9DcOhjEs6GNMap5A6UI+ByOuUdLLJiOR+GJ\nQ7E/5KGnCBq+JgLfJEsGeKojNMLRyPhtYgxmXrDuIIx/HhcIxP2VPzDlSvBqYl9t\nqgbb7NL5CLbWO4szW1h1JIfxCbKN/Q1eafZAlXH8Rbkksowfjun406P+kGM3E4KP\nFnCrA97E3dlf9QX2f2WTF+XVIwWAP575sCz1EFzR8PMXfpoHZq/ufQxjdEkyCvGs\nhh0WN5A1AgMBAAECggEAHXsqUkM9aVuCQelrKye5VdVVPmMUAUmJ9wobBJ5MYWIY\n2DIu98MMW0cVSbrku30Nic1mzygopqLLRJoAWhhUVV4DWKUmQUimOHVoboYNrzNA\nrZPvNmShMCipP/NjxxJ/mu71VAyAKe5idqeR46gjREFl2jp4r1F5N8x4nwI1RxVj\n1cHsPMyZqcdJYatmOAL+u46kHMNuyo2KwXFauLT3DSRpuBPW3SRWoySEBWAp8Qxj\nemfOREdK1gw17e+prSb2+4cN6WYmOWKWaN2mRNFaf6bwkvE6pvVaiVvjD6rx39iQ\nXtCtxtd9gqtAG57eeTTkdryZaBzMhdZ5zTZPi1SqWwKBgQD9M09rlp8dgK5JJZBN\naqfYTdAdgDKzgdybE2+4Dzl9UVR/fL9VRs6z0RwHsUVQLGMtRDAvpHNkhrTsIueo\nZSNyxqerV/9nA4Kvpm9Boi1iy4LAB6So8Br3HCSRu54i0qLSZSf0QhpQkzsCWdEc\n+bo5AP/JnGNsPlGiiNShfocYywKBgQC7oDfUiiSlhwTwpgQoa2uG2yNmw3aLazNa\nIb74KV5s2faO/pGkBKQOeAQ+Qc2rvCOUuFhrt7HnKsRmUrXD+iL57n3ptudZIbT/\nhnVp9gARQtn7F5P6hSHMMItJGFna5rIM4Z1qDAzFXZZJ4FXXcBEQHwuWClJjJquv\nEM6KK3va/wKBgQCGEftFztWl+5NNrBRCyeziPiGq3Uz7fBHiE2KepYEdeEkz0ExH\nzVx6HomnERjQoRBK0cZqE7v+SM3YE4tywUsJ5WK2+buFQniapZhXupYpr/Ul1WY9\nBhZhLoe2mw/bBImuul1zmuTwMWWXkxOFMj6HHJ5UlPiYQk9brvRYJvVGDQKBgGmD\n2OH2LlXIcMbFFmGEx5u3cVlBY1FUoDR39eWpniipCzevgkgzM+/PHtPEPd3umDPy\n2Ab771iJfJnuubnU2gakULs22TQO+LMa8rz8U11hsyS6RcYFSNSEGFCrGR05z7fe\nyZ/x1tzHnNU/DAd0RqRCUUm31E1eWf7B/OVHPwgRAoGADfNuuriXdIyZqgQna1FZ\na2pEtQS9OWZb7gwvjhHc1n5OYk27ToUpxaUstvUmvN+zqVFXuRhDMmw2hbecAZvd\nUbcglQ5L4HZNAuMylS1Ou9Ev6tf98J1iAO0KM+WtMd8rCjEhQg6FVVH0VR0mHq5c\ndNIzpBr3Qm8FW4c+K6f4xZg=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-gm5qw@onyumbanihousing-1cc4d.iam.gserviceaccount.com",
  "client_id": "114816838177636306086",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gm5qw%40onyumbanihousing-1cc4d.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(credential=cred, options={'storageBucket': 'onyumbanihousing-1cc4d.appspot.com'})
bucket = storage.bucket()

# cred = credentials.Certificate("./src/service_key_onyumbani.json")
from src.controllers import *

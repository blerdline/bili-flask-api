import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
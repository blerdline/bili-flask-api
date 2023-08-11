import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from database import Database
from datetime import datetime

import logging

load_dotenv()

class FirebaseDatabase(Database):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialize_firebase_app()
        return cls.__instance

    def _initialize_firebase_app(self):
        logging.info('Initializing Firebase connection')
        service_account_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
        cred = credentials.Certificate(service_account_key)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        logging.info('Firebase connection initialized..')

    def get_collection_data(self, collection, uid):
        doc_ref = self.db.collection(collection).document(uid)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return data
        else:
            return None
        
    def get_collection_reference(self, collection, uid):
        doc_ref = self.db.collection(collection).document(uid)
        doc = doc_ref.get()
        if doc.exists:
            return doc_ref
        else:
            return None
        
    def add_customer(self, customer_id):
    
        cust_data = { "phoneNumber": customer_id, "verified": False, "createdTime": datetime.now(), "langPref": None, "createdAt": datetime.now()}
        cust_doc_ref = self.db.collection('users').document(customer_id)
        cust_doc = cust_doc_ref.get()
        if cust_doc.exists:
            return "Customer Already exists"
        else:
            #Add customer to database
            cust_doc_ref.set(cust_data)
            return f'Customer {customer_id} added'
        
    def update_language(self, customer_id, language):
        language_data = {"langPref": language}
        cust_ref = self.db.collection('users').document(customer_id)
        cust_ref.set(language_data, merge=True)
        return f'Language updated to {language}'




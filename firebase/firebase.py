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
        
    def get_user_invoice_ref(self, user_id):
        return self.db.collection('users').document(user_id).collection('invoices')
        
    def add_customer(self, customer_id):
    
        cust_data = { 
            "phoneNumber": customer_id, 
            "verified": False, 
            "createdTime": datetime.now(), 
            "langPref": None, 
            "createdAt": datetime.now(), 
            "subscribed": False
        }
        cust_doc_ref = self.db.collection('users').document(customer_id)
        cust_doc = cust_doc_ref.get()
        if cust_doc.exists:
            return "Customer Already exists"
        else:
            #Add customer to database
            cust_doc_ref.set(cust_data)
            return f'Customer {customer_id} added'
        
    def update_language(self, customer_id, language):
        language_data = {
            "langPref": language, 
            "updatedAt": datetime.now()
        }
        cust_ref = self.db.collection('users').document(customer_id)
        cust_ref.set(language_data, merge=True)
        return f'Language updated to {language}'
    
    def update_subscription(self, customer_id, subscribed):
        subscription_data = {
            "subscribed": subscribed,
            "updatedAt": datetime.now()
        }
        cust_ref = self.db.collection('users').document(customer_id)
        cust_ref.set(subscription_data, merge=True)
        return f'Subscription updated to {subscribed}'
    
    def add_invoice(self, customer_id, customer_name, line_items):
        
        invoice_data = {
            "createdAt": datetime.now(),
            "customerName": customer_name,
            "invoiceTotal": 0
        }

        invoice_ref = self.db.collection('users').document(customer_id).collection('invoices').document()
        invoice_ref.set(invoice_data)
        for line_item in line_items:
            line_item_data = {
                "createdAt": datetime.now(),
                **line_item
            }
            invoice_line_item_ref = invoice_ref.collection('line_items').document()
            invoice_line_item_ref.set(line_item_data)
        return f'Invoice {invoice_ref.id} added'

    def update_invoice_total(self, customer_id, invoice_id, total):
        invoice_data = {
            "total": total,
            "updatedAt": datetime.now()
        }
        invoice_ref = self.db.collection('users').document(customer_id).collection('invoices').document(invoice_id)
        invoice_ref.set(invoice_data, merge=True)
        return f'Invoice {invoice_id} updated'
    
    def add_line_item(self, customer_id, invoice_id, line_item_data):
        line_item_data['createdAt'] = datetime.now()
        invoice_line_item_ref = self.db.collection('users').document(customer_id).collection('invoices').document(invoice_id).collection('line_items').document()
        invoice_line_item_ref.set(line_item_data)
        return f'Line item {invoice_line_item_ref.id} added'
    
    def edit_line_item(self, customer_id, invoice_id, line_item_id, line_item_data):
        line_item_data['updatedAt'] = datetime.now()
        invoice_line_item_ref = self.db.collection('users').document(customer_id).collection('invoices').document(invoice_id).collection('line_items').document(line_item_id)
        invoice_line_item_ref.set(line_item_data, merge=True)
        return f'Line item {line_item_id} edited'
    


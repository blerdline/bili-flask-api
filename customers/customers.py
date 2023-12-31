import firebase_admin
from firebase_admin import firestore
from firebase import firebase
from datetime import datetime

from firebase.firebase import FirebaseDatabase
from language_service import LanguageService
from invoice.invoice import Invoice

class Customer:
    database = FirebaseDatabase()
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.language_service = LanguageService(self.database)

    def update_language(self, language):
        return self.language_service.update_language(self.customer_id, language)

    def get_customer_data(self) -> dict or None:
        return self.database.get_collection_data('users', self.customer_id)

        
    def can_customer_create_invoice(self) -> bool:

        #Customer can create an invoice in the following cases:
        # 1. If the customer is subscribed or
        # 2. If the customer is verified and have created less than 4 invoices
        customer_data = self.get_customer_data()
        if not customer_data:
            return False
        
        trial_limit = self.database.get_collection_data('free_trial', 'expiration')['free_trial_limit']

        verified = customer_data.get('verified', False)
        invoice_count = self.count_invoices()
        subscribed = customer_data.get('subscribed', False)

        if subscribed or (verified and invoice_count <= trial_limit):
            return True
        else:
            return False    
    
    def calculate_invoice_total(self, line_items) -> float:
        total = 0
        for line_item in line_items:
            total += line_item.get('price', 0) * line_item.get('quantity', 0)
        return total
        
    def get_invoice_line_items(self, invoice_id) -> list:
        line_items = []

        invoice_line_items_ref = self.database.get_collection_reference(f'users/{self.customer_id}/invoices/{invoice_id}/line_items')
        # invoice_line_items_ref = self.db.collection('users').document(self.customer_id).collection('invoices').document(invoice_id).collection('line_items').get()

        for line_item in invoice_line_items_ref:
            line_item_data = line_item.to_dict()
            line_item_data['id'] = line_item.id # Add line Item ID to the data
            line_items.append(line_item_data)                      

        return line_items
        
    def get_invoices(self) -> list:
        invoices = []
        invoices_ref = self.database.get_collection_reference(f'users/{self.customer_id}/invoices')
        #invoices_ref = self.db.collection('users').document(self.customer_id).collection('invoices').get()
        print(self.count_invoices())
        for invoice in invoices_ref:
            invoice_data = invoice.to_dict()
            invoice_data['id'] = invoice.id  # Add invoice ID to the data dictionary
            line_items = self.get_invoice_line_items(invoice.id)  # Get line items for the invoice
            invoice_data['line_items'] = line_items
            total = self.calculate_invoice_total(line_items)
            invoice_data['calculated_total'] = total
            invoices.append(invoice_data)

        return invoices
    
    def count_invoices(self):
        invoices = []
        customer_ref = self.database.get_collection_reference('users', self.customer_id)
        invoices_ref = customer_ref.collection('invoices').get()
        
        return len(invoices_ref)
    
    def get_single_invoice(self, invoice_id):
        invoice = self.db.collection('users').document(self.customer_id).collection('invoices').document(invoice_id).get()
        invoice_data = invoice.to_dict()
        invoice_data['id'] = invoice.id
        line_items = self.get_invoice_line_items(invoice.id)
        invoice_data['line_items'] = line_items
        total = self.calculate_invoice_total(line_items)
        invoice_data['calculated_total'] = total
        return invoice_data
    
    def add_invoice(self, customer_name, line_items):
        invoice = self.database.add_invoice(self.customer_id, customer_name, line_items)
        # invoice_ref = self.db.collection('users').document(self.customer_id).collection('invoices').document(invoice_id)
        # invoice_ref.set(invoice_data)
        return invoice
    
    def delete_invoices(self):
        invoice_ref = self.database.get_user_invoice_ref(self.customer_id)

        documents = invoice_ref.stream()

        for document in documents:
            document.reference.delete()

        return f'Invoices deleted'
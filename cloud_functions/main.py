from google.cloud import firestore


# Initialize the Firestore client
db = firestore.Client()

# Cloud Function to update the counter when a document is added to /users/{user_id}/invoices
def increment_invoice_counter(context):
    user_id = context.params['user_id']
    counter_doc_ref = db.collection('users').document(user_id).collection('counters').document('invoices_counter')
    counter_doc_ref.update({'count': firestore.Increment(1)})

# Cloud Function to update the counter when a document is removed from /users/{user_id}/invoices
def decrement_invoice_counter(context):
    user_id = context.params['user_id']
    counter_doc_ref = db.collection('users').document(user_id).collection('counters').document('invoices_counter')
    counter_doc_ref.update({'count': firestore.Increment(-1)})

# Cloud Function to update the counter when a document is added to /users/{user_id}/invoices/{invoice_id}/line_items
def increment_items_counter(context):
    user_id = context.params['user_id']
    invoice_id = context.params['invoice_id']
    counter_doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('counters').document('line_items_counter')
    counter_doc_ref.update({'count': firestore.Increment(1)})

# Cloud Function to update the counter when a document is removed from /users/{user_id}/invoices/{invoice_id}/line_items
def decrement_items_counter(context):
    user_id = context.params['user_id']
    invoice_id = context.params['invoice_id']
    counter_doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('counters').document('line_items_counter')
    counter_doc_ref.update({'count': firestore.Increment(-1)})

def generate_numeric_id(user_id):
    # Get the current counter value from the 'counters' document for the specified user
    counter_doc_ref = db.collection('users').document(user_id).collection('counters').document('numeric_id_counter')
    counter_data = counter_doc_ref.get().to_dict()
    current_counter = counter_data.get('count', 0)

    # Increment the counter for the specified user
    counter_doc_ref.update({'count': firestore.Increment(1)})

    # Use the counter as the numeric ID
    return current_counter + 1

def create_invoice_document(data,user_id):
    # Generate the numeric ID for the specified user
    numeric_id = generate_numeric_id(user_id)

    # Set the document with the generated numeric ID in the 'invoices' collection of the specified user
    doc_ref = db.collection('users').document(user_id).collection('invoices').document(numeric_id)
    document_data = { **data }
    doc_ref.set(document_data)

def generate_numeric_line_item_id(user_id, invoice_id):
    # Get the current counter value from the 'counters' document for items under the specified invoice
    counter_doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('counters').document('line_items_counter')
    counter_data = counter_doc_ref.get().to_dict()
    current_counter = counter_data.get('count', 0)

    # Increment the counter for items under the specified invoice
    counter_doc_ref.update({'count': firestore.Increment(1)})

    # Use the counter as the numeric item ID
    return current_counter + 1

def create_line_item_document(data, context):
    # Access the wildcard segments from the context
    user_id = context.params.get('user_id')
    invoice_id = context.params.get('invoice_id')

    # Generate the numeric item ID for the specified user and invoice
    numeric_item_id = generate_numeric_line_item_id(user_id, invoice_id)

    # Set the item document with the generated numeric item ID in the 'line_items' collection under the specified invoice
    doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('line_items').document(numeric_item_id)
    document_data = { **data }
    doc_ref.set(document_data)

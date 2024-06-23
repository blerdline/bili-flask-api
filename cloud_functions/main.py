from google.cloud import firestore
import functions_framework
from cloudevents.http.event import CloudEvent


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

def count_documents_in_collection(collection_ref):
    count = 0
    for doc in collection_ref.stream():
        count += 1
    return count

def count_invoices(user_id):
    invoices_ref = db.collection('users').document(user_id).collection('invoices')
    return count_documents_in_collection(invoices_ref)

@functions_framework.cloud_event
def count_documents(cloud_event: CloudEvent):
    event_data = cloud_event.data
    print(f"Received CloudEvent with data: {event_data}")

    if 'documents' in event_data:
        doc_count = len(event_data['documents'])
        print(f"Number of documents: {doc_count}")
    else:
        print("No documents found in the event data")
        
# def count_documents(cloud_event: CloudEvent):
#     print(cloud_event)
#     user_id = cloud_event.data['user_id']
#     # user_id = context.params['user_id']
#     invoices_count = count_invoices(user_id)
#     return invoices_count



# def generate_numeric_id(user_id):
#     # Get the current counter value from the 'counters' document for the specified user
#     user_ref = db.collection('users').document(user_id)
#     counter_doc_ref = user_ref.collection('counters').document('numeric_id_counter')
#     counter_data = counter_doc_ref.get().to_dict()
#     if counter_data is not None:
#         current_counter = counter_data.get('count', 0)
#     else:
#         current_counter = 0
#         counter_doc_ref.set({'count': 0})
        
#     # Increment the counter for the specified user
#     counter_doc_ref.update({'count': firestore.Increment(1)})

#     # Use the counter as the numeric ID
#     return current_counter + 1

# def create_invoice_document(data,context):

#     value_data = data.get('value')  # Access the nested 'value' dictionary
#     processed_flag = value_data.get('fields', {}).get('processed',{}).get('stringValue')
#     if processed_flag == 'yes':
#         return

#     # Generate the numeric ID for the specified user
#     path_parts = context.resource.split('/documents/')[1].split('/')
#     user_id = path_parts[1]
#     original_invoice_id = path_parts[3]
#     numeric_id = str(generate_numeric_id(user_id))
    
#     extracted_data = {
#         'createdAt': value_data.get('fields', {}).get('createdAt', {}).get('timestampValue'),
#         'customerName': value_data.get('fields', {}).get('customerName', {}).get('stringValue'),
#         'invoiceTotal': value_data.get('fields', {}).get('invoiceTotal', {}).get('integerValue')
#     }

#     extracted_data['processed'] = 'yes'
#     # Set the document with the generated numeric ID in the 'invoices' collection of the specified user
#     doc_ref = db.collection('users').document(user_id).collection('invoices').document(numeric_id)
#     doc_ref.set(extracted_data)
#     original_doc_ref = db.collection('users').document(user_id).collection('invoices').document(original_invoice_id)
#     #original_doc_ref.delete()
#     return numeric_id

# def generate_numeric_line_item_id(user_id, invoice_id):
#     # Get the current counter value from the 'counters' document for items under the specified invoice
#     counter_doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('counters').document('line_items_counter')
    
#     user_invoice_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id)
#     counter_doc_ref = user_invoice_ref.collection('counters').document('numeric_id_counter')
#     counter_data = counter_doc_ref.get().to_dict()
    
#     if counter_data is not None:
#         current_counter = counter_data.get('count', 0)
#     else:
#         current_counter = 0
#         counter_doc_ref.set({'count': 0})

#     # Increment the counter for items under the specified invoice
#     counter_doc_ref.update({'count': firestore.Increment(1)})

#     # Use the counter as the numeric item ID
#     return current_counter + 1

# def create_line_item_document(data, user_id, invoice_id, batch=None):

#     # print(data)
#     # value_data = data.get('value')
#     # processed_flag = value_data.get('fields', {}).get('processed',{}).get('stringValue')
#     # if processed_flag == 'yes':
#     #     return

#     # Access the wildcard segments from the context
#     # path_parts = context.resource.split('/documents/')[1].split('/')
#     # user_id = path_parts[1]
#     # invoice_id = path_parts[3]

#     print("Line Item Data: ", data)
#     # print("Line Item Contenxt: ", context)
#     # Generate the numeric item ID for the specified user and invoice
#     numeric_item_id = str(generate_numeric_line_item_id(user_id, invoice_id))

#     # extracted_data = {
#     #     'createdAt': value_data.get('fields', {}).get('createdAt', {}).get('timestampValue'),
#     #     'description': value_data.get('fields', {}).get('description', {}).get('stringValue'),
#     #     'amount': value_data.get('fields', {}).get('amount', {}).get('integerValue'),
#     #     'price': value_data.get('fields', {}).get('price', {}).get('floatValue')
#     # }

#     data['processed'] = 'yes'

#     # extracted_data['processed'] = 'yes'
         
#     # Set the item document with the generated numeric item ID in the 'line_items' collection under the specified invoice
#     doc_ref = db.collection('users').document(user_id).collection('invoices').document(invoice_id).collection('line_items').document(numeric_item_id)
#     #document_data = { **data }
    
#     if batch:
#         batch.set(doc_ref, data)
#     else:
#         doc_ref.set(data)


# def migrate_invoice_and_line_items(data, context):
#     # Migrate the invoice and line items
#     new_invoice_id = create_invoice_document(data, context)
    
#     path_parts = context.resource.split('/documents/')[1].split('/')
#     user_id = path_parts[1]
#     original_invoice_id = path_parts[3]

#     line_items_collection_ref = db.collection('users').document(user_id).collection('invoices').document(original_invoice_id).collection('line_items')
#     line_items = line_items_collection_ref.stream()

#     old_invoice_ref = db.collection('users').document(user_id).collection('invoices').document(original_invoice_id)
#     batch = db.batch()
    
#     old_line_items = []  # Store the old line items

#     for line_item_doc in line_items:
#         old_line_items.append(line_item_doc.to_dict())  # Store the old line item data
#         batch.delete(line_item_doc.reference)
    
#     # Commit the batched line item deletions
#     batch.commit()
    
#     batch = db.batch()
    
#     # Now, migrate the stored old line items in a batch
#     for line_item_data in old_line_items:
#         create_line_item_document(line_item_data, user_id, new_invoice_id, batch=batch)
    
#     # Commit the batched line item migrations
#     batch.commit()

#     # Delete the old invoice
#     old_invoice_ref.delete()


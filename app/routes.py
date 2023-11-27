from flask import jsonify, request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from app.helpers.helpers import convert_escape_chars
from customers.customers import Customer
#from app import app
from text_parser import parse_text_message, parse_modify_line_item_text, parse_delete_line_item_text, parse_insert_line_item_text, parse_invoice_number_text
from firebase.firebase import FirebaseDatabase
import os

twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

firebase = FirebaseDatabase()
users_bp = Blueprint('users', __name__, url_prefix='/users')
customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

test = {}
test['basic'] = {
    "to": '+18318511377', # Test Twilio Number
    "from": '+15125551212', # Test Customer
    "body": "@Just Me\n#Try one repair $50 1\n#Get three at half off $25 3"
}
test['delete'] = {
    "to": '+18318511377', # Test Twilio Number
    "from": '+15125551212', # Test Customer
    "body": "-2\n-3"
}
test['add'] = {
    "to": '+18318511377', # Test Twilio Number
    "from": '+15125551212', # Test Customer
    "body": "#Immersted in the Playstation $43.28 2"
}
test['edit'] = {
    "to": '+18318511377', # Test Twilio Number
    "from": '+15125551212', # Test Customer
    "body": ">5 Lamps $12 3\n>2 Chairs $25 2"
}
test['invoice'] = {
    "to": '+18318511377', # Test Twilio Number
    "from": '+15125551212', # Test Customer
    "body": "Invoice 3\n"
}


bp = Blueprint('routes', __name__)
@bp.route('/')
def index():
    print('In index')
    return jsonify({'message': 'Welcome to your Flask API!'})

@bp.route('/invoice_test', methods=['POST', 'GET'])
def invoice_test():
    test_message = test['invoice']
    body = test_message['body']
    response = parse_invoice_number_text(body)
    print(response)
    return jsonify(response)

@bp.route('/modify_invoice_items', methods=['POST', 'PUT'])
def modify_invoice_items():
    test_message = test['edit']
    body = test_message['body']
    response = parse_modify_line_item_text(body)
    print(response)
    return jsonify(response)

@bp.route('/delete_invoice_items', methods=['POST', 'DELETE'])
def delete_invoice_items():
    test_message = test['delete']
    body = test_message['body']
    response = parse_delete_line_item_text(body)
    print(response)
    return jsonify(response)

@bp.route('/insert_invoice_items', methods=['POST', 'PUT'])
def insert_invoice_items():
    test_message = test['add']
    body = test_message['body']
    response = parse_insert_line_item_text(body)
    print(response)
    return jsonify(response)

     
@bp.route('/sms', methods=['POST', 'GET'])
def sms():

    from_number = request.form['From']
    to_number = request.form['To']
    # test_message = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "@Just Me\n#Try one repair $50.00 1\n#Get three at half off $25.00 3"
    # }

    # test_message_1 = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "Invoice 1"
    # }

    # test_message_2 = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "Edit Invoice 1"
    # }

    # test_message_3 = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "Help"
    # }

    # test_message_4 = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "English"
    # }

    # test_message_5 = {
    #     "to": '+18318511377', # Test Twilio Number
    #     "from": '+15125551212', # Test Customer
    #     "body": "Español"
    # }


    # I want to dispatch to the right function based on the message body using a dispatch pattern
    # message_body = {
    #     '@': add_customer,
    #     '#': get_invoice,
    #     'edit': edit_invoice,
    #     'invoice': get_invoice,
    #     'help': get_help_text,
    #     'english': set_language,
    #     'español': set_language
    # }


    # I want to route to the right function based on the message using a dictionary
    # message_type = {
    #     'welcome': get_welcome_text,
    #     'language_confirmation': get_language_confirmation,
    #     'invoice': get_invoice,
    #     'edit_invoice': edit_invoice,
    #     'help': get_help_text
    # }

    # message_type['welcome']()


    # If the message is from the Test Customer and that Customer is not in the database or the language is not set, send the welcome message
    if not Customer(from_number).get_customer_data() or not Customer(from_number).get_customer_data().get('langPref'):
        # Send the welcome message
        welcome_message = get_welcome_text()
        print(welcome_message)
        welm_text = welcome_message['text']
        # twilio_client.messages.create(
        #     to=from_number,
        #     from_=to_number,
        #     body=welm_text
        # )
        return welm_text
    

    if 'Body' in request.form:
        data = request.form['Body']
    else:
        data = request.data.decode('utf-8')

    print(data)
    user_id = request.form['From']

    #if free trial is over, send a message to upgrade
    trial_message = get_free_trial_expiration(user_id)
    if trial_message['free_trial_expired']:
        return trial_message['message']

    customer_name, line_items = parse_text_message(data)

    customer = Customer(user_id)
    response_text = customer.add_customer(user_id)
    print(response_text)
    response = MessagingResponse()
    # response.message(response_text)
    # we need to check the customer exist
    # we need to check if the customer has multiple invoices


    return str(response)

@bp.route('/language_confirmation', methods=['POST'])
def set_language():

    if 'Body' in request.form:
        data = request.form['Body']
    else:
        data = request.data.decode('utf-8')

    user_id = request.form['From']
    customer = Customer(user_id)
    # Make sure data is either 'English' or 'Español'
    

    response_text = customer.update_language(user_id, data)
    print(response_text)
    response = MessagingResponse()
    response.message(response_text)
    return str(response)


@users_bp.route('/<user_id>', methods=['GET'])
def get_user_data(user_id):
    data = firebase.get_collection_data('users',user_id)
    if data:
        return {'data': data}
    else:
        return {'error': 'User not found'}
    
@users_bp.route('/<user_id>/statement', methods=['GET'])
def get_user_statement(user_id):
    pass

@users_bp.route('/<user_id>/invoice', methods=['GET'])
def get_user_invoices(user_id):
    customer = Customer(user_id)
    customer_invoice = customer.get_invoices()

    if customer_invoice:
        return customer_invoice
    else:
        return {'error': 'Customer Invoice could not be found'}
    
@users_bp.route('/<user_id>/free-trial-expiration', methods=['GET'])
def get_free_trial_expiration(user_id):
    '''
    This endpoint should return a message for signing up for a paid subscription once the free trial has expired
    Free trial expiration should be configurable, and should be stored in the database
    The default free trial will be 3 invoices
    '''

    #check number of invoices for the user.  If greater than 3, send message to sign up for paid subscription
    customer = Customer(user_id)
    customer_invoice = customer.count_invoices()
    data = customer.get_customer_data()

    customer_subscription = data['subscribed']
    lang_pref = data['langPref']

    free_invoice_limit = firebase.get_collection_data('free_trial','expiration')

    if customer_subscription == True:
        return {'message': 'You are subscribed', 'free_trial_expired': True, 'customer_subscription': True}

    if customer_invoice > free_invoice_limit['free_trail_limit']:
        free_trial_expired = firebase.get_collection_data('communications','free_trial_expired')
        free_trial_expired = convert_escape_chars(free_trial_expired[lang_pref])
        return {'message': free_trial_expired, 'free_trial_expired': True, 'customer_subscription': False}
    else:
        return {'message': 'You have not reached your free trial limit', 'free_trial_expired': False, 'customer_subscription': False}
    
@users_bp.route('/<user_id>/subscription-confirmation', methods=['GET'])
def get_subscription_confirmation(user_id):


    pass


'''
When a user sends a text message to the Twilio number, and they are not registered nor have a valid language set,
the app should respond with a welcome message, asking them which language they want to continue in.

The welcome message should be configurable, and should be stored in the database

Currently the message will look like this:
Hola, welcome to Bili! We can’t wait to start helping you with your invoices.
To continue in English, text “English”.
To continue in Spanish, text “Español”.
'''
@bp.route('/welcome-text', methods=['GET'])
def get_welcome_text():
    
    data = firebase.get_collection_data('communications','welcome_text')
    data = convert_escape_chars(data['text'])
    if data:
        return {'text': data}
    else:
        return {'error': 'Welcome text not found'}


'''
After a user has set their language, the app should respond with a message 

Welcome to Bili, let’s get started.
To subscribe for unlimited invoices, sign up here: LINK
To create an invoice, reply with “Invoice”.
To edit an invoice, reply with “Edit Invoice” and the invoice number you want to edit. For example: “Edit Invoice 3”.
If you need help with something else email us at dev@bilibiz.com.

'''
@bp.route('/language-confirmation', methods=['POST'])
def get_language_confirmation():
    pass

'''

'''




# API Documentation

This API is built using Flask and Twilio for handling SMS-based invoice management.

## Endpoints

### /

- Method: GET
- Description: Welcome endpoint for the API.

### /invoice_test

- Method: POST, GET
- Description: Test endpoint for invoice functionality.

### /modify_invoice_items

- Method: POST, PUT
- Description: Endpoint for modifying invoice items.

### /delete_invoice_items

- Method: POST, DELETE
- Description: Endpoint for deleting invoice items.

### /insert_invoice_items

- Method: POST, PUT
- Description: Endpoint for inserting new invoice items.
### /users/<user_id>/invoice

- Method: DELETE
- Description: Endpoint for deleting all invoices for a specific user.

### /sms

- Method: POST, GET
- Description: Endpoint for handling SMS messages.

### /language_confirmation

- Method: POST
- Description: Endpoint for setting the language preference for a user.

### /users/<user_id>

- Method: GET
- Description: Endpoint for retrieving user data.

### /users/<user_id>/invoice

- Method: GET, POST
- Description: Endpoint for retrieving all invoices for a user or creating a new invoice.

### /users/<user_id>/invoice/<invoice_id>

- Method: GET
- Description: Endpoint for retrieving a specific invoice for a user.

### /users/<user_id>/invoice/<invoice_id>/line_items

- Method: GET
- Description: Endpoint for retrieving line items for a specific invoice.

### /users/<user_id>/free-trial-expiration

- Method: GET
- Description: Endpoint for checking the expiration of a user's free trial.

### /users/<user_id>/subscription-confirmation

- Method: GET
- Description: Endpoint for confirming a user's subscription status.

### /welcome-text

- Method: GET
- Description: Endpoint for retrieving the welcome text.

## Setup
To run this API, you will need to set the following environment variables:

- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN

## Testing
This API includes a set of predefined test messages that can be used to test its functionality. These are stored in the test dictionary.

## Dependencies
This API uses the following Python libraries:

- Flask
- Twilio
- firebase_admin

Please ensure these are installed before running the API.

## Contact
For any issues, please contact the developer at [dev@bilibiz.com](mailto:dev@bilibiz.com).

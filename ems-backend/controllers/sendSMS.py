import os
from twilio.rest import Client
from flask import jsonify

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure


def sendPassword(_employee_id, _password: str, phone_number:str):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    print("FLLLLLAAAG", account_sid, auth_token, os.environ)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=f'Hello, your employee_id is {_employee_id} and password is: {_password}',
                                from_='+17752568881',
                                to=phone_number
                            )
    if message.error_code is not None:
        return False, "Failed verification"
    
    return True, f"Sent successfully with sid: {message.sid}"

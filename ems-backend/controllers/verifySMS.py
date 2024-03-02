import os
from twilio.rest import Client
from flask import jsonify

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure


def verify(phone_number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    verification = client.verify \
                     .services('VAf7d752e72d603e81693e678145b6c43c') \
                     .verifications \
                     .create(to=phone_number, channel='sms')
    return jsonify({
        "status": f"Sent verification code to number {verification.to}", 
        "is_validated": False
    })


def checkVerify(OTP:str, phone_number: str):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
                           .services('VAf7d752e72d603e81693e678145b6c43c') \
                           .verification_checks \
                           .create(to=phone_number, code=OTP)
    if verification_check.status == "approved":
        return jsonify({
            "status": "OTP Verified successfully", 
            "verified": True
        })
    else:
        return jsonify({
            "status": "Unsuccessful verification", 
            "verified": False
        })

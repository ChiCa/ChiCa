from twilio.rest import TwilioRestClient
import os
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(body="Jenny please?! I love you <3",
    to="+13618160814",    # Replace with your phone number
    from_="+18447079094") # Replace with your Twilio number
print message.sid
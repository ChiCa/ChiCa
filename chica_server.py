from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import os
 
app = Flask(__name__)
numbers = {"+1361XXXXXXX":["+1510XXXXXXX", "+1361XXXXXXX"]}

#Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(account_sid, auth_token)


@app.route("/", methods=['GET', 'POST'])
# def hello_world():
#     return 'Hello World!'

def start():
	"""Respond to incoming requests."""

	resp = twilio.twiml.Response()
	from_number = request.values.get('From', None)
	if from_number in numbers:
		return redirect("/registered-user")
	else:
		numbers[from_number] = []
		with resp.gather(numDigits=12, action="/sign-up", method="POST") as g:
 			g.say("Welcome to cheeka. Cheeka helps you build a circle of mothers who exchange child care. To sign up and start a cheeka circle, type in the phone number of a mother you trust who lives nearby after the beep.", voice="woman")
 	return str(resp)

@app.route("/sign-up", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    friend_number = request.values.get('Digits', None)
    numbers["+13618160814"].append(friend_number)
    
    resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        # If the dial fails:
    resp.say("Thank you for signing up! You are now part of the ChiCa community. We will now forward you to the main menu or your can hang up now.", voice="woman")
    return redirect("/registered-user")

@app.route("/registered-user", methods=['GET', 'POST'])
def request_care():
	resp = twilio.twiml.Response()
	with resp.gather(numDigits=1, action="/decision", method="POST") as g:
 		g.say("To request child care, press zero. To add a mother who lives near you, press one.", voice="woman")
 	return str(resp)

@app.route("/decision", methods=['GET', 'POST'])
def decision():
	choice = request.values.get('Digits', None)
	if choice == "0":
          return redirect("/choose-day")
	elif choice == "1":
		return redirect("/add-friend")
	else:
		return redirect("/registered-user")

@app.route("/choose-day", methods=['GET', 'POST'])
def choose_day():
	resp = twilio.twiml.Response()

	with resp.gather(numDigits=1, action="/send-text-messages", method="POST") as g:
 		g.say("If you need child care tomorrow, press zero. If you need child care the day after tomorrow, press one.", voice="woman")
 	return str(resp)

@app.route("/send-text-messages", methods=['GET', 'POST'])
def send_text_messages():
	choice = request.values.get('Digits', None)
	resp = twilio.twiml.Response()
	if choice == "0":
		return redirect("/tommorrow-text")
	elif choice == "1":
		return redirect ("/day-after-tommorrow-text")
	else:
		resp.say("I am sorry, I did not understand.")
		return redirect("/choose-day")

@app.route("/tommorrow-text", methods=['GET', 'POST'])
def send_tommorrow_text():
    #msg_to_list = numbers.values()
    #for number in msg_to_list:
    # message = client.messages.create(body="A ChiCa in your circle needs child care tommorrow.  Can you help her?",
    #     to=+"+15104849529",    # Replace with your phone number
    #     from_="+18447079094") # Replace with your Twilio number
	message = client.messages.create(body="A ChiCa needs child care tomorrow. Can you help her? Call +1 844-XXX-XXXX to hear her request.",
    	to="+1510XXXXXXX",
    	from_="+1844XXXXXXX")
	#resp = twilio.twiml.Response()
	print message.sid
	return redirect("/record-message")
	# resp.say("cheeka is requesting child care from your circle.")
	# resp.sms("A ChiCa in your circle needs child care tommorrow.  Can you help her?", To="+15104849529", From="+18447079094")
	# return str(resp)

@app.route("/day-after-tommorrow-text", methods=['GET', 'POST'])
def send_day_after_text():

	message = client.messages.create(body="A cheeka in your circle needs child care the day after tommorrow. Can you help her? Call +1 844-707-9094 to hear her request.",
    	to="+15104849529",
    	from_="+18447079094")
	print message.sid
	return redirect("/record-message")

@app.route("/add-friend", methods=['GET', 'POST'])
def add_friend():
	resp = twilio.twiml.Response()

	with resp.gather(numDigits=12, action="/confirm-add", method="GET") as g:
		g.say("To add a mother who lives near you to your cheeka circle, enter her phone number.", voice="woman")
	return str(resp)

@app.route("/confirm-add", methods=['GET', 'POST'])
def confirm_add():
	resp = twilio.twiml.Response()

	new_friend = request.values.get('Digits', None)
	numbers["+13618160814"].append(new_friend)
	resp.say("Thank you for adding your friend to your cheeka circle! She is now part of the cheeka community. Call cheeka back to request child care", voice="woman")
	# with resp.gather(numDigits=0, action="/registered-user", method="GET") as g:
	# 	g.say("Thank you for adding your friend to your chica circle! She is now part of the chica community. We will now forward you to the child care request menu, or you can hang up.", voice="woman")
	return str(resp)
	#return redirect("/registered-user")

@app.route("/record-message", methods=['GET', 'POST'])
def record_message(): 
	resp = twilio.twiml.Response()
	resp.say("Record a message for your care giver after the tone. In your message, please confirm you will bring food for your children and a little extra for the cheeka", voice="woman")
	resp.record(maxLength="10", action="/handle-recording")
	return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
	"""Play back the caller's recording."""

	recording_url = request.values.get("RecordingUrl", None)

	resp = twilio.twiml.Response()
	resp.say("Cheeka will now play back your recording", voice="woman")
	resp.play(recording_url)
	resp.say("Thank you for using cheeka! Cheeka has requested child care from your circle. You will receive a confirmation and contact information soon. Goodbye.", voice="woman")
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

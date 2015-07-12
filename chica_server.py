from flask import Flask, request, redirect
import twilio.twiml


app = Flask(__name__)
numbers = []


@app.route("/", methods=['GET', 'POST'])
# def hello_world():
#     return 'Hello World!'

def hello_monkey():
	"""Respond to incoming requests."""
	resp = twilio.twiml.Response()
	from_number = request.values.get('From', None)
	numbers.append(from_number)
	with resp.gather(numDigits=12, action="/sign-up", method="POST") as g:
 		g.say("Welcome to ChiCa. ChiCa help you build a network of mothers who can exchange child care among eachother. To signup to the ChiCa community type in the number of your friend after the beep.")
 	return str(resp)

@app.route("/sign-up", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    friend_number = request.values.get('Digits', None)
    numbers.append(friend_number)
    
    resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        # If the dial fails:
    resp.say("Thank you for signing up! You are now part of the ChiCa community. We will now forward you to the main menu or your can hang up now.")
 
    return str(resp) 

if __name__ == "__main__":
    app.run(debug=True)
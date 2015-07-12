from flask import Flask
import twilio.twiml

from flask.ext.heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

@app.route("/", methods=['GET', 'POST'])
# def hello_world():
#     return 'Hello World!'


def hello_monkey():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello Monkey")
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)
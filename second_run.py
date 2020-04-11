import os
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

cwd = os.getcwd()
DOWNLOAD_DIRECTORY = cwd
app = Flask(__name__)

account_sid = 'AC0f3a55e06e1960f649a31d00778c1b1b'
auth_token = 'ca9ac1a946dc611155998a6db4bcd14c'
client = Client(account_sid, auth_token)

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""

    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if request.values['NumMedia'] != '0':

        # Use the message SID as a filename.
        filename = request.values['MessageSid']+'.jpg'
        with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
           image_url = request.values['MediaUrl0']
           f.write(requests.get(image_url).content)
           f.close()

        resp.message("Thanks for your contribution to WILDNET!")
    else:
        resp.message("Try sending us a picture message.")

    return str(resp)

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug= True)

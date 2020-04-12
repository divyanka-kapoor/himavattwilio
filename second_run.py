import os
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
import logging
import wget
import urllib.request
import boto3
from io import StringIO
import contextlib


cwd = os.getcwd()
DOWNLOAD_DIRECTORY = cwd

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="./service_account.json"


app = Flask(__name__)

account_sid = 'ACa4a4839e8c88a2d4250621d942f5f1f7'
auth_token = '2d18ca3fedb5260ae4869cb2ec8ecd56'
client = Client(account_sid, auth_token)

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""

    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if request.values['NumMedia'] != '0':

        # Use the message SID as a filename.
        filename = request.values['MessageSid']+'.jpg'
        bucket_name = "semiotic-creek-273921.appspot.com"
        source_file_url = request.values['MediaUrl0']
        s3 = boto3.resource('s3')
        bucket_name_to_upload_image_to = 'himavat'


        req_for_image = requests.get(source_file_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()

        s3.Bucket(bucket_name_to_upload_image_to).put_object(Key=filename, Body=req_data)

        resp.message("Thanks for your contribution to WILDNET!")
    else:
        resp.message("Try sending us a picture message.")

    return str(resp)

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug= True)

import os
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from google.cloud import storage
import logging
import wget

# cwd = os.getcwd()
# DOWNLOAD_DIRECTORY = cwd

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
        bucket_name = "staging.semiotic-creek-273921.appspot.com"
        source_file_name = request.values['MediaUrl0']

        def upload_blob(bucket_name, source_file_name, filename):
            """Uploads a file to the bucket."""

            filename = wget.download(source_file_name)
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_filename(filename, content_type='image/jpg')
            os.remove(filename)

        upload_blob(bucket_name, source_file_name, filename)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, filename
            )
        )
        # def create_file(self, filename):
        #     self.response.write('Creating file %s\n' % filename)
        # write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        # gcs_file = gcs.open(filename,
        #               'wb',
        #               retry_params=write_retry_params)
        # image_url = request.values['MediaUrl0']
        # gcs_file.write(requests.get(image_url).content)
        # gcs_file.write('f'*1024*4 + '\n')
        # gcs_file.close()
        # self.tmp_filenames_to_clean_up.append(filename)
        # with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
        #
        #    f.write(requests.get(image_url).content)
        #    f.close()

        resp.message("Thanks for your contribution to WILDNET!")
    else:
        resp.message("Try sending us a picture message.")

    return str(resp)

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug= True)

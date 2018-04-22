from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests
from requests.auth import HTTPBasicAuth
from PIL import Image
import os
import label_image

app = Flask(__name__)
size = 299, 299
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    #blocking call. Returns a reponse when someone texts here
    resp = MessagingResponse()
    media_url = request.form['MediaUrl0']
    print(media_url)
    # Save the image to a new file.
    filename = request.form['MessageSid'] + '.png'
    with open('{}/{}'.format('./', filename), 'wb') as f:
        image_url = request.form['MediaUrl0']
        f.write(requests.get(image_url, auth=HTTPBasicAuth('ACddf07758130a0e67b3a0a8f800430937', '920e519dda86709f3fd16c89d7083e96')).content)
        f.close()
    im = Image.open('{}/{}'.format('./', filename))
    im.thumbnail(size,Image.ANTIALIAS)
    rgb_im = im.convert('RGB')
    rgb_im.save('{}/{}.jpg'.format('./', filename))
    os.remove('{}/{}'.format('./', filename))
    ret = label_image.start_recognizing('{}/{}.jpg'.format('./', filename))
    print(ret)
    resp.message(ret)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

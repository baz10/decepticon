import random
import requests
import os
from flask import Flask, request
from pymessenger.bot import Bot
 
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
SimsimiKey = os.environ['SimsimiKey']
bot = Bot(ACCESS_TOKEN) 

 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET': 
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:

       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):

                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    userMessage = message['message'].get('text')
                    response_sent_text = get_message(userMessage)
                    send_message(recipient_id, response_sent_text)

                if message['message'].get('attachments'):
                    response_sent_nontext = get_message(1)
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):

    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'





#chooses a random message to send to the user
def get_message(userMessage):
    
    URL = "http://sandbox.api.simsimi.com/request.p?key={}&lc=id&ft=1.0&text={}".format(SimsimiKey, userMessage)
    r = requests.get(url = URL)
    data = r.json()

   # print (data)
    if data == 509:
       	return data['msg']
    else:
        return data['response']

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
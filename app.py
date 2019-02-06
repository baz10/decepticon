import random
import requests
import os

from flask import Flask, request
from pymessenger.bot import Bot
 
app = Flask(__name__)
ACCESS_TOKEN = "EAADWjJgyWIABAAwnwRYxBQl3sJZBKh1h0ZBd6NrhfpX0d7ZA2KU7GufYWmtf8Y8MrF4481aBikPQpsajLlzaxbHCY83FpgZAvRCUrv1kRnnOr16OnVssw9kPywBnb0PyTGJybEdOwNQ31gtntchepLF48fM8YE3I1OnyWQW5BwZDZD"#os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = "decepticon"#os.environ['VERIFY_TOKEN']
SimsimiKey = "90a9e3ae-527a-4055-86d8-4275ae9ccb69"#os.environ['SimsimiKey']
bot = Bot(ACCESS_TOKEN) 

 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
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
    
    URL = "http://sandbox.api.simsimi.com/request.p?key={}&lc=id&ft=1.0&text={}".format(SimsimiKey,userMessage)
    r = requests.get(url = URL)
    data = r.json()
    if data['result'] == 1:
        return data['response']
    else:
        print ("Yikes! Something Went Wrong..")


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
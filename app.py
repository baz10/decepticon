import random, json, pyowm, apiai
import requests
import os
from Utils import NLP
from flask import Flask, request
from pymessenger.bot import Bot
 
app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
SimsimiKey = os.environ['SimsimiKey']
OWM_KEY = os.environ['OWM_KEY']
CLIENT_ACCESS_TOKEN = os.environ['APIAI_CLIENT_ACCESS_TOKEN']


owm = pyowm.OWM(OWM_KEY)
bot = Bot(ACCESS_TOKEN) 
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
 
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
                    response_sent_text = parse_user_text(message['message'].get('text'))
                    #print(response_sent_text)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = parse_user_text(1)
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def parse_user_text(user_text):
    request_ai = ai.text_request()
    request_ai.query = user_text

    response = json.loads(request_ai.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    if (responseStatus == 200):
        if('intentName' in response['result']['metadata'].keys()):
            if(response['result']['metadata']['intentName'] == 'Current Weather'):
                input_city = response['result']['parameters']['geo-city']
                return get_weather(input_city)
            else:
                return response['result']['fulfillment']['speech']
        else:
            return response['result']['fulfillment']['speech']
    else:
         return("Yikes! Brains not found")


def get_weather(city):  
    
    try:
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        max_temp = str(w.get_temperature('celsius')['temp_max'])  
        min_temp = str(w.get_temperature('celsius')['temp_min'])
        current_temp = str(w.get_temperature('celsius')['temp'])
        wind_speed = str(w.get_wind()['speed'])
        humidity = str(w.get_humidity())
        weather_report = ' max temp: ' + max_temp + ' min temp: ' + min_temp + ' current temp: ' + current_temp + ' wind speed :' + wind_speed + ' humidity ' + humidity + '%'
        return weather_report
    except Exception as e:
        print(e) 



def verify_fb_token(token_sent):

    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'



'''def get_message(userMessage):
     if NLP.isAskingBotInformation(userMessage):
        return NLP.handleBotInfo(userMessage)
     URL = "http://sandbox.api.simsimi.com/request.p?key={}&lc=en&ft=1.0&text={}".format(SimsimiKey,userMessage)
    r = requests.get(url = URL)
    data = r.json()
    if data['result'] == 100:
        return data['response']
    else:
        return data['msg'] '''


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
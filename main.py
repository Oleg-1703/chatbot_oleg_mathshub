import telebot
import requests
from constants import token
from constants import api_key

url = "https://api.edenai.run/v2/image/generation"

#website for connecting to artificial intelligence
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """a welcome letter asking the user to make a request"""
    bot.reply_to(message,"Write your text to generate an image")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """generating an image based on the user's request "message_text" by connecting via api_key"""
    bot.send_message(message.from_user.id, "wait a second")
    
    payload = {
    "providers": "replicate",
    "text": message.text,
    "resolution": "512x512",
    "fallback_providers": ""
    }
    
    headers = {"Authorization": f"Bearer {api_key   }"}
    response = requests.post(url, json=payload, headers=headers)
    res = response.text
    index1 = res.find('https')
    index2 = res.find('.png') + 4
    res2 = res[index1:index2]
    if res2 != "": #in case of successful decryption of the link
      bot.send_message(message.from_user.id, res2)
    else: #in case of error and missing link
      bot.send_message(message.from_user.id, "Error. Try again")

bot.infinity_polling()
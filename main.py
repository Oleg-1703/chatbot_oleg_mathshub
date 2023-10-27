import telebot
import requests
import json
import re
from constants import token
from constants import api_key

url = "https://stablediffusionapi.com/api/v3/dreambooth"
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
    payload = json.dumps({
    "key": api_key, #api key for connection
    "model_id": "realistic-vision-v40", #version of AI
    "prompt": message.text,
    #user request
    "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
    #keywords exceptions
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": "30",
    "safety_checker": "no",
    "enhance_prompt": "yes",
    "seed": None,
    "guidance_scale": 7.5,
    "multi_lingual": "no",
    "panorama": "no",
    "self_attention": "no",
    "upscale": "no",
    "embeddings": "embeddings_model_id",
    "lora": "lora_model_id",
    "webhook": None,
    "track_id": None
    })

    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)

    res = re.sub(r'\\', '', response.text) #the link to the picture, encrypted in characters
    index1 = res.find('https')
    index2 = res.find('g"],') + 1
    res2 = res[index1:index2]
    #decryption, link selection
    if res2 != "": #in case of successful decryption of the link
        bot.send_message(message.from_user.id, res2)
    else: #in case of error and missing link
        bot.send_message(message.from_user.id, "Error. Try again")

bot.infinity_polling()
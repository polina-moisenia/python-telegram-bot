import os
import telebot
import re

API_KEY = os.environ['TELEGRAM_API_KEY']
bot = telebot.TeleBot(token=API_KEY)

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Welcome, honey :)')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'This bot is searching for specific words...')

@bot.message_handler(func=lambda msg: msg.text is not None)
def at_converter(message):
    msg = re.split("\W+", message.text)
    temp_list = []
    for i in msg:
        if len(i) == 4:
            temp_list.append(i.lower())
    if temp_list:
        bot.reply_to(message, "I found the following words: " + " ".join(temp_list))
    if not temp_list:
        bot.reply_to(message, "I haven't found any words")

bot.polling()
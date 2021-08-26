import os
import telebot

API_KEY = os.environ['TELEGRAM_API_KEY']
bot = telebot.TeleBot(token=API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome, honey :)')

bot.polling()
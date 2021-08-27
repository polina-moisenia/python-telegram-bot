import os
import telebot
import re
import paho.mqtt.client as mqtt

##################MQTT##################

broker = "127.0.0.1"
port = 1883
client_id = 'python-mqtt-telegram-bot'
topic = "/python/mqtt"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

mqtt.Client.connected_flag = False

def publish_to_mqtt(client, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic `{topic}`")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()

##################BOT##################

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
    # temp_list = []
    for i in msg:
        if len(i) == 4:
            # temp_list.append(i.lower())
            if client.connected_flag == True:
                publish_to_mqtt(client, i.lower())
    # if temp_list:
    #     bot.reply_to(message, "I found the following words: " + " ".join(temp_list))        
    # else:
    #     bot.reply_to(message, "I haven't found any words")

bot.polling()
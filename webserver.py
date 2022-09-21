from collections import UserList
import os
import shutil
import telebot
import requests as req
from datetime import date, timedelta
from datetime import datetime
from flask import Flask
from threading import Thread
import funs as mf
import time


app = Flask('')

try:
    import test
    key = test.API_KEY
    url = test.WEB_URL
    user_list = test.user_list

except:
    key = os.environ["API_KEY"]  # ! "YOUR_API_KEY"
    # ! The website from where the data is fetched.
    url = os.environ["WEB_URL"]
    user_list = []
    user_list.append(os.environ["USER2"])
    user_list.append(os.environ["USER1"])
    group_list = []
    group_list.append(os.environ["USER3"])
bot = telebot.TeleBot(key)


@app.route('/')
def home():
    return "I'm alive"

#! ======================== Daily Paper Distribution ======================


def send_all_chat():
    filename = mf.todays_filename()
    mf.log(f"Sending {filename} to all the users...")
    for user in user_list:
        with open(filename, 'rb') as f:
            bot.send_document(user, f)
            f.close()


def send_all_group():
    filename = mf.todays_filename()
    mf.log(f"Sending {filename} to all the groups...")
    for group in group_list:
        with open(filename, 'rb') as f:
            bot.send_document("-100"+group, f)
            f.close()


@app.route('/dailysend')
def dailysend():
    filename = mf.todays_filename()
    if os.path.exists(filename):
        t_chat = Thread(target=send_all_chat)
        t_group = Thread(target=send_all_group)
        t_chat.start()
        t_group.start()
    else:
        mf.download_latest_paper()
        t_chat = Thread(target=send_all_chat)
        t_group = Thread(target=send_all_group)
        t_chat.start()
        t_group.start()
        try:
            yester_file = mf.yesterdays_filename()
            shutil.move(yester_file, "prevPaper/" + yester_file)
        except:
            pass
    return "Sent"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

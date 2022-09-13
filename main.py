import os
import time
import shutil
import telebot
import urllib.request
import requests as req
from datetime import date
from datetime import timedelta

key = os.environ["API_KEY"]  # ! "YOUR_API_KEY"
bot = telebot.TeleBot(key)


def download_paper(url):
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    filename = "The_Hindu_" + d4 + ".pdf"
    urllib.request.urlretrieve(url, filename)
    return filename


def paper_fun(message):
    tt = message.text.lower()
    if ("paper" in tt or "hindu" in tt):
        return True
    else:
        return False


@bot.message_handler(commands=['greet'])
def greet(message):
    name = message.text.split()[1]
    bot.reply_to(message, f"Hi {name} what's up")
    print(message.text)


@bot.message_handler(commands=[
    'paper',
    'hindu',
    'newspaper',
])
def hindu(message):
    bot.delete_message(message.chat.id, message.id)
    bb = bot.send_message(
        message.chat.id, message.from_user.first_name +
        ", We are Uploading the file !!\n============================= \n\nPlease Wait....... "
    )
    try:
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        filename = "The_Hindu_" + d4 + ".pdf"
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
            bot.delete_message(bb.chat.id, bb.id)
    except:
        # ! The website from where the data is fetched.
        url = os.environ["WEB_URL"]
        res = req.get(url)
        a = res.text.split("<td>")
        latest_paper = a[20].split("</td>")[0]
        latest_paper_link = req.get(latest_paper).text.split(
            "iframe")[3].split('"')[2]

        filename = download_paper(latest_paper_link)

        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
            bot.delete_message(bb.chat.id, bb.id)

        yesterday = date.today() - timedelta(days=1)
        d4 = yesterday.strftime("%b-%d-%Y")
        file = "The_Hindu_" + d4 + ".pdf"
        try:
            shutil.move(file, "prevPaper/"+file)
        except:
            pass
    # os.remove(filename)


print("running....", time.time())

bot.polling()

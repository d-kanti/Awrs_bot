import os
import glob
import shutil
import telebot
import calendar
import urllib.request
import requests as req
from datetime import date
from datetime import datetime
from datetime import timedelta
# from webserver import keep_alive

# keep_alive()

# getting enviromentals, bot token & web url
try:
    import test
    key = test.API_KEY
    url = test.WEB_URL
except:
    key = os.environ["API_KEY"]  # ! "YOUR_API_KEY"
    url = os.environ["WEB_URL"]  # ! The website from where the data is fetched.

bot = telebot.TeleBot(key)


#function to log
def log_user(message):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    user = str(message.from_user.first_name) + " " + str(
        message.from_user.last_name)
    uid = message.from_user.id
    chat = message.chat.id

    st = f"[ {time} ] - {message.text} ||  user: {user} ({uid})   chat id : {chat}\n"

    print(st)
    with open("log.text", "a") as f:
        f.write(st)


def log(text):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st = f"[ {time} ] - {text}\n"

    print(st)
    with open("log.text", "a") as f:
        f.write(st)


# downloads the paper
def download_paper(url):
    log("Downloading Paper.....")
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    filename = "The_Hindu_" + d4 + ".pdf"
    urllib.request.urlretrieve(
        url, filename)  #Download file from url with following filename
    log("Download Complete !!")
    return filename


def mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return True
    return False


def mon_inv(message):
    return True


def get_mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return i


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
    log_user(message)
    bot.delete_message(message.chat.id, message.id)
    bb = bot.send_message(
        message.chat.id, message.from_user.first_name +
        ", We are Uploading the file !!\n============================= \n\nPlease Wait....... "
    )
    try:
        log("Trying to upload Previously Downloaded file.....")
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        filename = "The_Hindu_" + d4 + ".pdf"
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
            bot.delete_message(bb.chat.id, bb.id)
    except:
        log("No file found.")
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
            shutil.move(file, "prevPaper/" + file)
        except:
            pass
    log("Upload Complete....\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        )


@bot.message_handler(func=mon)
def month_pap(message):
    log_user(message)
    m = get_mon(message)
    log(f"getting files ready for the month of {m}")    
    bb = bot.send_message(message.chat.id,f"hi {message.from_user.first_name}, Please Wait.....\n\nWe are preparing your files... \n\n\nTill then.... Let's Grab a Coffee.. ☕😁")
    file_pref = "The_Hindu_"+m
    for filename in glob.glob(file_pref+"-??-????.pdf"):
        with open(filename, 'rb') as f:
            log(f"sending file '{filename}'")
            bot.send_document(message.chat.id, f)
    for filename in glob.glob("prevPaper/"+file_pref+"-??-????.pdf"):
        with open(filename, 'rb') as f:
            log(f"sending file '{filename}'")
            bot.send_document(message.chat.id, f)
    bot.delete_message(bb.chat.id, bb.id)
    log("Uploade Complete.....\n++++++++++++++++++++++++++++++++++++++++++++++++++++++")

 



print("running....", datetime.now())

bot.polling()

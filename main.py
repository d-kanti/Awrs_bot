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
    # ! The website from where the data is fetched.
    url = os.environ["WEB_URL"]

bot = telebot.TeleBot(key)

# function to Log the User


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

# Function to keep Log


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
        url, filename)  # Download file from url with following filename
    log("Download Complete !!")
    return filename

# check if any month mensoned in the message


def mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return True
    return False

# Always True


def mon_inv(message):
    return True

# Get the name of the month, mensioned in the message.


def get_mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return i

# Greeting to anyone.


@bot.message_handler(commands=['greet'])
def greet(message):
    name = message.text.split()[1]
    bot.reply_to(message, f"Hi {name} what's up")
    print(message.text)

#! ======================== Paper Distribution ======================
# gets the most recent paper and sends to the user.


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

#! ======================== Monthly Paper Distribution ======================
# gets the papers of a whole month, and send them to the user.


@bot.message_handler(func=mon)
def month_pap(message):
    log_user(message)
    m = get_mon(message)
    log(f"getting files ready for the month of {m}")
    file_pref = "The_Hindu_" + m
    filelist = glob.glob("prevPaper/" + file_pref + "-??-????.pdf")
    filelist = filelist + glob.glob(file_pref + "-??-????.pdf")
    if (len(filelist) < 1):
        bot.send_message(
            message.chat.id,
            "SORRY !!   😢 \n\n There are no files for the following month...")
        log("No files to send.... Task Complete !! \n++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            )
    else:
        bb = bot.send_message(
            message.chat.id,
            f"hi {message.from_user.first_name}, Please Wait.....\n\nWe are preparing your files... \n\n\nTill then.... Let's Grab a Coffee.. ☕😁"
        )
        cc = bot.send_message(
            message.chat.id,
            f"FIles Uploading\n==============\n\nProgress:  [[ {0}/{len(filelist)} ]]"
        )

        for i in range(len(filelist)):
            filename = filelist[i]
            with open(filename, 'rb') as f:
                log(f"sending file '{filename}'")
                bot.send_document(message.chat.id, f)
                bot.edit_message_text(
                    text=f"FIles Uploading\n==============\n\nProgress:  [[ {i+1}/{len(filelist)} ]]",
                    message_id=cc.message_id,
                    chat_id=cc.chat.id)

        bot.edit_message_text(
            text=f"FIles Uploaded\n==============\n\nProgress:  [ ✅ ]",
            message_id=cc.message_id,
            chat_id=cc.chat.id)
        bot.delete_message(bb.chat.id, bb.id)

    log("Uploade Complete..... \n++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        )


#! ======================== /start  or  /help ===========================
#   If the Command is not recognized, a helping message is sent to the user.

@bot.message_handlers(commands=['start', 'help'])
def help(message):
    log_user(message)
    bot.send_message(
        text="Please use folloing commands\n==============================\n\n\n /paper -> get Latest Paper Available\n\n\n/September -> Get Papers for the month of September.",
        chat_id=message.chat.id)
    log("Sending the helping message....\nTask Completed....\n++++++++++++++++++++++++++++++++++++")

#! ======================== Unrecognized Command ===========================
#   If the Command is not recognized, a helping message is sent to the user.


@bot.message_handler(lambda message: True)
def dn(message):
    log_user(message)
    log("Command not Recognized.  Sending the helping message....\nTask Completed....\n++++++++++++++++++++++++++++++++++++")
    bot.send_message(
        text="Please use folloing commands\n==============================\n\n\n /paper -> get Latest Paper Available\n\n\n/September -> Get Papers for the month of September.",
        chat_id=message.chat.id)


log("running....")

bot.polling()

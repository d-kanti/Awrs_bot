import os
import glob
import shutil
import telebot
import calendar
import funs as mf
import urllib.request
import requests as req
from datetime import date
from datetime import datetime
from datetime import timedelta
from webserver import keep_alive

keep_alive()

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


#! ======================== Paper Distribution ======================


# gets the most recent paper and sends to the user.
@bot.message_handler(commands=[
    'paper',
    'hindu',
    'newspaper',
])
def hindu(message):
    mf.log_user(message)
    bot.delete_message(message.chat.id, message.id)
    bb = bot.send_message(
        message.chat.id, message.from_user.first_name +
        ", We are Uploading the file !!\n============================= \n\nPlease Wait....... "
    )
    try:
        mf.log("Trying to upload Previously Downloaded file.....")
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        filename = "The_Hindu_" + d4 + ".pdf"
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
            bot.delete_message(bb.chat.id, bb.id)
    except:
        mf.log("No file found.")
        res = req.get(url)
        a = res.text.split("<td>")
        latest_paper = a[20].split("</td>")[0]
        latest_paper_link = req.get(latest_paper).text.split(
            "iframe")[3].split('"')[2]

        filename = mf.download_paper(latest_paper_link)

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
    mf.log("Upload Complete....\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
           )

#! ======================== Monthly Paper Distribution ======================


# gets the papers of a whole month, and send them to the user.
@bot.message_handler(func=mf.mon)
def month_pap(message):
    mf.log_user(message)
    m = mf.get_mon(message)
    mf.log(f"getting files ready for the month of {m}")
    file_pref = "The_Hindu_" + m
    filelist = glob.glob("prevPaper/" + file_pref + "-??-????.pdf")
    filelist = filelist + glob.glob(file_pref + "-??-????.pdf")
    if (len(filelist) < 1):
        bot.send_message(
            message.chat.id,
            "SORRY !!   😢 \n\n There are no files for the following month...")
        mf.log("No files to send.... Task Complete !! \n++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
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
                mf.log(f"sending file '{filename}'")
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

    mf.log("Uploade Complete..... \n++++++++++++++++++++++++++++++++++++++++++++++++++++++"
           )


#! ======================== /start  or  /help ===========================


#   If the Command is not recognized, a helping message is sent to the user.
@bot.message_handler(commands=['start', 'help'])
def help(message):
    mf.log_user(message)
    bot.send_message(
        text="Please use folloing commands\n==============================\n\n\n /paper -> get Latest Paper Available\n\n\n/September -> Get Papers for the month of September.",
        chat_id=message.chat.id)
    mf.log("Sending the helping message....\nTask Completed....\n++++++++++++++++++++++++++++++++++++")

#! ======================== Unrecognized Command ===========================


#   If the Command is not recognized, a helping message is sent to the user.
@bot.message_handler(func=lambda message: True)
def dn(message):
    mf.log_user(message)
    bot.send_message(
        text="Please use folloing commands\n==============================\n\n\n /paper -> get Latest Paper Available\n\n\n/September -> Get Papers for the month of September.",
        chat_id=message.chat.id)
    mf.log("Command not Recognized.  Sending the helping message....\nTask Completed....\n++++++++++++++++++++++++++++++++++++")


mf.log("running....")

bot.polling()

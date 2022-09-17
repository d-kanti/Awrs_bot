import calendar
import urllib.request
from datetime import date
from datetime import datetime


#! function to Log the User
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


#! Function to keep Log
def log(text):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st = f"[ {time} ] - {text}\n"

    print(st)
    with open("log.text", "a") as f:
        f.write(st)


#! downloads the paper from the website
def download_paper(url):
    log("Downloading Paper.....")
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    filename = "The_Hindu_" + d4 + ".pdf"
    urllib.request.urlretrieve(
        url, filename)  # Download file from url with following filename
    log("Download Complete !!")
    return filename


# ? check if any month mensoned in the message
def mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return True
    return False


# ! Get the name of the month, mensioned in the message.
def get_mon(message):
    t = message.text
    for i in calendar.month_abbr:
        if i.lower() in t.lower() and len(i.lower()) == 3:
            return i

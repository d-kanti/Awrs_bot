import calendar
import urllib.request
from datetime import date, timedelta
from datetime import datetime
import requests as req
import os


try:
    import test
    # key = test.API_KEY
    url_paper_web = test.WEB_URL
    # user_list = test.user_list

except:
    # key = os.environ["API_KEY"]  # ! "YOUR_API_KEY"
    # ! The website from where the data is fetched.
    url_paper_web = os.environ["WEB_URL"]
    # user_list = [os.environ["USER1"], os.environ["USER2"]]


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

    filename = todays_filename()
    # Download file from url with following filename
    urllib.request.urlretrieve(url, filename)
    log("Download Complete !!")

def download_latest_paper():
    log("Downloading Paper.....")

    filename = todays_filename()
    latest_paper_link = get_latest_paper_link()
    # Download file from url with following filename
    urllib.request.urlretrieve(latest_paper_link, filename)
    log("Download Complete !!")


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


def get_latest_paper_link():

    res = req.get(url_paper_web)
    a = res.text.split("<td>")

    today_list = todays_filename().split("_")[2].split("-")
    today_list[2] = today_list[2].split(".")[0]

    for i in a[2:]:
        if today_list[0] in i and today_list[1] in i and today_list[2] in i:
            tod_ind = a.index(i)+1
            break
    print("index is ",tod_ind)
    latest_paper = a[tod_ind].split("</td>")[0]
    latest_paper_link = req.get(latest_paper).text.split(
        "iframe")[3].split('"')[2]
    return latest_paper_link


def todays_filename():
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    filename = "The_Hindu_" + d4 + ".pdf"
    return filename


def yesterdays_filename():
    yesterday = date.today() - timedelta(days=1)
    d4 = yesterday.strftime("%b-%d-%Y")
    filename = "The_Hindu_" + d4 + ".pdf"
    return filename

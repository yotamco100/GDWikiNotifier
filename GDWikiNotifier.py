# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from pushbullet import PushBullet
import time
from datetime import datetime
import logging

#save logs
logging.basicConfig(filename="WikiNotifier-Log.txt", level=logging.DEBUG)

logging.info("Starting up!")
print("[{}] Starting up!".format(datetime.now()))

#my pushbullet token
pb = PushBullet("YOUR_ACCESS_TOKEN_HERE")

#website interaction
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' #user agent just so bs4 won't be a cunt
url = "http://wiki.gamedetectives.net/index.php?title=Waking_Titan" # url to pull from
headers={'User-Agent':user_agent} #dictionary that Requests can read
response = requests.get(url,headers=headers) #open the requested webpage
soup = BeautifulSoup(response.text, "lxml") #create a soup object of the response
tocDivContent = soup.find("div", { "class" : "toc" }) #find the table of contents
tocContent = tocDivContent.findChildren() #find the contents of the table of contents
lastTOCEntry = tocContent[-1].contents[0] #find the last content entry's content of the table of contents
logging.info("Last TOC entry as of startup: " + lastTOCEntry) #just logs

#loop for getting future changes
while(True):
    print("[{}] Checking for changes...".format(datetime.now()))
    logging.info("Checking...")
    response = requests.get(url,headers=headers) #open the requested webpage
    soup = BeautifulSoup(response.text, "lxml") #create a soup object of the response
    tocDivContent = soup.find("div", { "class" : "toc" })
    tocContent = tocDivContent.findChildren()
    newTOCEntry = tocContent[-1].contents[0]
    if (newTOCEntry != lastTOCEntry):
        print("[{}] Change found! Pushing...".format(datetime.now()))
        logging.info("New Section! Pushing...")
        push = pb.push_link("Waking Titan Wiki Update - " + newTOCEntry, "http://wiki.gamedetectives.net/index.php?title=Waking_Titan")
        lastTOCEntry = newTOCEntry
        print("[{}] Pushed!".format(datetime.now()))
    else:
        print("[{}] Nothing found yet! Checking in 15 mins...".format(datetime.now()))
        logging.info("No changes found! Checking in 15 mins...")
    time.sleep(900)

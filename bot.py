from dotenv import load_dotenv
from bs4 import BeautifulSoup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import re
import os

import http.server
import socketserver

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'new.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()
load_dotenv() 
def download_image(url: str):
 
    # post request to server

    api = os.environ.get('API_POST')
    myobj = {
        'link': url}

    x = requests.post(api, data=myobj)
    # grab image from response

    soup = BeautifulSoup(x.text, 'html.parser')

    img=soup.find('div', id='downloadBox').findAll('a')


    return img
def sdownload_story(url: str,num:int):


    api = os.environ.get('API_STORY')

    url=url.replace(str(num), "")
    link=url.replace(" ",'')
    myobj = {'username': link}

    x = requests.post(api, data = myobj)
    # grab image from response

    soup = BeautifulSoup(x.text, 'html.parser')
    num=int(num)-1
    try:
        content=soup.find('div', id='downloadBox').findAll('a')[num]['href']
    except AttributeError as aerror:
        return 0
    else:
        return content


def sstory(update: Update, context: CallbackContext):
    uuid = update.message.text.replace("/ss", "")
    try:
        if(uuid.__len__()!=0):
            num=int(uuid[1])
            if(uuid==''):
                update.message.reply_text("Please use command /ss <URL>")
                
            else:
                update.message.reply_text("Proccessing... ETA: 20 Seconds")
                img = sdownload_story(uuid,num)
                if img ==0:
                    update.message.reply_text("Sorry, this story is not available! May be it is a private account, or it is not a story, or the user doesnot have "+num+' stories')
                else:
                    update.message.reply_video(img)
        else:
            update.message.reply_text("Enter the correct command syntax - /ss <story number of user> <username without @>")
    except:
        update.message.reply_text("Enter the correct command syntax - /ss <story number of user> <username without @>") 

    
    
        
# post request to server 
def download_story(url: str):
    api = os.environ.get('API_STORY')
    if(url.startswith('https://www')):
        link=url.replace("https://www.instagram.com/stories/","")
        res = link[:link.index('/') + len('/')]
        res=res.replace('/', '')
        res=res.replace(' ', '')
        print(res)
        myobj = {'username': res}
        x = requests.post(api, data = myobj)
        # grab image from response

        soup = BeautifulSoup(x.text, 'html.parser')
        try:
            content=soup.find('div', id='downloadBox').findAll('a')
        except AttributeError as aerror:
            return 0
        else:
            return content

        
    else:
        link=url.replace("https://instagram.com/stories/","")
        res = link[:link.index('/') + len('/')]
        res=res.replace('/', '')
        res=res.replace(' ', '')
        myobj = {'username': res}
        x = requests.post(api, data = myobj)
        # grab image from response

        soup = BeautifulSoup(x.text, 'html.parser')
        try:
            content=soup.find('div', id='downloadBox').findAll('a')
        except AttributeError as aerror:
            return 0
        else:
            return content
        
        
        


    





updater = Updater(os.environ.get('TOKEN'),use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /post <URL> - To download instagram posts (Url must start with http:// or https://)
    /ss <story number> <username without @> - To download single story of a user)
    /story <any story link of user> - To download all stories of a user
    /help - To see the this menu""")
def download(update: Update, context: CallbackContext):
    uuid = update.message.text.replace("/post", "")
    if(uuid==''):
        update.message.reply_text("Please use command /post <URL>")

    else:
        if(uuid.startswith(' http')):
           

            update.message.reply_text("Proccessing... Please wait for 20 seconds")
            img = download_image(uuid)
            for i in img:
                try:
                    update.message.reply_video(i['href'])
                except:
                    update.message.reply_text("Ente Ponnadave! nee enth link aa thanne? Server adichu poyallo!!")
                
        else:
            update.message.reply_text("Please use command /post <URL> with a valid url starting with http:// Or https://")

def downloadstory(update: Update, context: CallbackContext):
    uuid = update.message.text.replace("/story", "")
    if(uuid==''):
        update.message.reply_text("Please use command /story <URL>") 
    else:
        
        if(uuid.startswith(' http')):
           

            update.message.reply_text("Downloading... ETA: 1 Minute")
            img = download_story(uuid)
            if img ==0:
                update.message.reply_text("Sorry, this story is not available! May be it is a private account, or it is not a story, or the url entered by you is not in the form of https://instagram.com/stories/<username>/<story_id>")
            else:
                for each in img:
                    link=each['href']
                    update.message.reply_video(link)
        else:
            update.message.reply_text("Please use command /story <URL> with a valid url starting with http:// Or https://")
        


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('post', download))
updater.dispatcher.add_handler(CommandHandler('story', downloadstory))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('ss', sstory))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
#start http server on port 3000

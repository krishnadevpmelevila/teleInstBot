from bs4 import BeautifulSoup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import re


def download_image(url: str):

    # post request to server

    api = 'https://instasave.website/insta-downloader'
    myobj = {
        'link': url}

    x = requests.post(api, data=myobj)
    # grab image from response

    soup = BeautifulSoup(x.text, 'html.parser')

    img=soup.find('div', id='downloadBox').find('img')['src']

    return img

# post request to server 
def download_story(url: str,num:int):
    print(num)

    api = 'https://instasave.website/instagram-stories-downloader'
    print(url.replace(" ", ""))
    myobj = {'username': url.replace(" ", "")}

    x = requests.post(api, data = myobj)
    # grab image from response

    soup = BeautifulSoup(x.text, 'html.parser')
    num=int(num)-1
    content=soup.find('div', id='downloadBox').findAll('a')[num]['href']
    return content





updater = Updater("5027109401:AAEl7fu-lG9c-LZF2WdtxmlkZkls34DxzC0",use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /download <URL> - To download instagram image/video/story (Url must start with http:// or https://)
    /help - To see the this menu""")
def download(update: Update, context: CallbackContext):
    uuid = update.message.text.replace("/download", "")
    if(uuid==''):
        update.message.reply_text("Please use command /download <URL>")
        update.message.reply_text(uuid)
    else:
        update.message.reply_text(uuid.startswith(' http'))
        
        if(uuid.startswith(' http')):
           

            update.message.reply_text("Downloading... ETA: 1 Minute")
            img = download_image(uuid)
            update.message.reply_photo(photo=img)
        else:
            update.message.reply_text(uuid)
            update.message.reply_text("Please use command /download <URL> with a valid url starting with http:// Or https://")

def downloadstory(update: Update, context: CallbackContext):
    uuid = update.message.text.replace("/downloadstory", "")
    num=int(uuid[1])
    print(uuid[1])
    if(uuid==''):
        update.message.reply_text("Please use command /download <URL>")
        update.message.reply_text(uuid)
    else:
        update.message.reply_text(uuid.startswith(' http'))
        update.message.reply_text("Downloading... ETA: 1 Minute")
        img = download_story(uuid,num)
        update.message.reply_video(img)
        


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('download', download))
updater.dispatcher.add_handler(CommandHandler('downloadstory', downloadstory))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()

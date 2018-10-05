#!/usr/bin/env python3

## code source: https://habr.com/post/346606/

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
import os
import logging

TOKEN_FILE="./TOKEN"
LOG_FILE="./bot.log"
vovels = 'аеийоуэя'

#logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

exists = os.path.isfile(TOKEN_FILE)
if exists:
    with open(TOKEN_FILE, "r") as t:
        mytoken=t.read().strip()
else:
    print("Token file %s not found" % TOKEN_FILE)
    sys.exit(1)

if not len(mytoken):
    print("Failed to read token from %s" % TOKEN_FILE)
    sys.exit(1)
else:
    logging.info('Token OK')

updater = Updater(token=mytoken) 
dispatcher = updater.dispatcher

def doLog(bot, update):
    logging.info(
            "CHAT: " + str(update.message.chat_id)
        + ". USER: " + str(update.message.from_user)
        + ". TEXT: " + str(update.message.text)
        )

def startCommand(bot, update):
    doLog(bot, update)
    bot.send_message(chat_id=update.message.chat_id, text='You shall not pass, ' + update.message.from_user)


def textMessage(bot, update):
    doLog(bot, update)
    response = 'GTFO'
    lastword = update.message.text.split(' ')[-1]
    for c in lastword:
        found = vovels.find(c)
        if not found == -1:
            pos = lastword.find(c)
            response = 'хуй' + lastword[pos+1:]
            break
    
    bot.send_message(chat_id=update.message.chat_id, text=response)

# handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# add handlers to dispatcher
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# start pooling updates
updater.start_polling(clean=True)

# Stop bot on Ctrl + C
updater.idle()

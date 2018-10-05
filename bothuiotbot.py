#!/usr/bin/env python3

## code source: https://habr.com/post/346606/

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
import os

TOKEN_FILE="./TOKEN"

vovels = 'аеийоуэя'

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
    #print("My token: %s" % mytoken)
    print("Token OK")

updater = Updater(token=mytoken) 
dispatcher = updater.dispatcher


def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='You shall not pass, ' + update.message.from_user)

def textMessage(bot, update):
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

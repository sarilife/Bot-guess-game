import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import bot_settings

from telegram import InlineKeyboardButton, ReplyKeyboardMarkup



MAX,MIN = 100,0
users = {}

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater(token=bot_settings.BOT_TOKEN)
dispatcher = updater.dispatcher





def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start command called by chat #{chat_id}")

    if chat_id not in users:
         users[chat_id] = {"a": MIN, "b": MAX,"guess":0,"explain":[], "history": [],"backdoor":[]}
    users[chat_id]['explain'] = []
    users[chat_id]['explain'].append("start the game")
    reply_markup = ReplyKeyboardMarkup([['Too high','Too low','Yes','Play Again']])
    bot.send_message(chat_id=chat_id, text="Welcome To guess game\nThe role of this game is simple ,\nfirst you should choose a number then I will try to guess it "
                                           "and then you will tell if is it to high or to low until I guess it\n\n\n is your number 50 ?"
    ,reply_markup = reply_markup)

def help(bot,update):
    chat_id = update.message.chat_id
    logger.info(f"> help command called by chat #{chat_id}")
    reply_markup = ReplyKeyboardMarkup([['New game','My history']])
    if chat_id not in users:
        return start(bot, update)

    bot.send_message(chat_id=chat_id, text="commands : \n /start\n/history",reply_markup = reply_markup)

def history(bot,update):
    chat_id = update.message.chat_id
    logger.info(f"> history command called by chat #{chat_id}")
    response = ""
    if chat_id not in users:
        return start(bot, update)

    if len(users[chat_id]["history"])==0:
        response += "you dont have history yet"
    else :
        for i,h in enumerate(users[chat_id]["history"]):
            response+=f"{i})  {h}\n"

    reply_markup = ReplyKeyboardMarkup([['New game','My history']])


    bot.send_message(chat_id=chat_id, text=response,reply_markup = reply_markup)


def explain(bot,update):
    chat_id = update.message.chat_id
    logger.info(f"> history command called by chat #{chat_id}")
    response = ""
    if chat_id not in users:
        return start(bot, update)

    if len(users[chat_id]["explain"])==0:
        response += "play game to explain it for you"
    else :
        for i,e in enumerate(users[chat_id]["explain"]):
            response+=f"{i+1})  {e}\n"

    reply_markup = ReplyKeyboardMarkup([['New game','My history']])


    bot.send_message(chat_id=chat_id, text=response,reply_markup = reply_markup)


def backdoor(bot,update):
    chat_id = update.message.chat_id
    logger.info(f"> history command called by chat #{chat_id}")
    response = ""
    if chat_id not in users:
        return start(bot, update)


    for i,b in enumerate(users[chat_id]["backdoor"]):
            response+=f"Game number #{i+1} \n-------------------\n"
            for j ,e in enumerate(b):
                 response+=f"{j+1}) {e}\n"

    reply_markup = ReplyKeyboardMarkup([['New game','My history']])


    bot.send_message(chat_id=chat_id, text=response,reply_markup = reply_markup)

def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= respond called by chat #{chat_id}: {text!r}")

    if chat_id not in users:
        return start(bot, update)

    if text == 'Too low':
        if users[chat_id]['b'] <= users[chat_id]['a'] :

            users[chat_id]['b'] = MAX
            users[chat_id]['a'] = MIN

            response = " you are playing with me Game over \n click on /start to play again "
        else :

            users[chat_id]['a'] = (users[chat_id]['a'] + (users[chat_id]['b']-users[chat_id]['a'])//2) +1
            users[chat_id]['guess']= users[chat_id]['a']
            users[chat_id]['explain'].append(f"Too low : your number is higher then {users[chat_id]['guess']}")
            response = f"is your number {users[chat_id]['guess']} ?"
    elif text == 'Too high':
        if users[chat_id]['b'] <=  users[chat_id]['a'] :
            users[chat_id]['b'] = MAX
            users[chat_id]['a'] = MIN
            response = " you are playing with me Game over \n click on /start to play again "
        else :
            users[chat_id]['b'] = (users[chat_id]['a'] + (users[chat_id]['b']-users[chat_id]['a']) //2) -1
            users[chat_id]['guess'] = users[chat_id]['b']
            users[chat_id]['explain'].append(f"Too high : your number is lower then {users[chat_id]['guess']}")
            response = f"is your number {users[chat_id]['guess']} ?"
    elif text == 'Yes':
        users[chat_id]['explain'].append(f"Yes : your number is  {users[chat_id]['guess']}")
        users[chat_id]['b'] = MAX
        users[chat_id]['a'] = MIN
        users[chat_id]['backdoor'].append(users[chat_id]['explain'])
        users[chat_id]['history'].append(f"You number was : {users[chat_id]['guess']}")
        response = "Perfect I guess it ,if you want to know how i guess it click on /explain"
    elif text == 'Play Again':
        return start(bot,update)
    elif text == "New game":
        return start(bot,update)
    elif text == "My history":
        return history(bot,update)
    else :
        response = "please type something readable or use my buttons below"

    reply_markup = ReplyKeyboardMarkup([['Too high','Too low','Yes','Play Again']])
    bot.send_message(chat_id=update.message.chat_id, text=response,reply_markup=reply_markup)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('history', history))
dispatcher.add_handler(CommandHandler('explain', explain))
dispatcher.add_handler(CommandHandler('backdoor', backdoor))

dispatcher.add_handler(MessageHandler(Filters.text,respond ))

logger.info("Start polling")
updater.start_polling()

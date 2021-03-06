import logging
#import telegram_id

from firebase import firebase

import private
import json

app = firebase.FirebaseApplication('https://food-exchange-a9870.firebaseio.com', None)


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
CallbackQueryHandler, RegexHandler, ConversationHandler)

TOKEN = private.key

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DATE, TIME, LOCATION, AMOUNT, MEAL, CONTACT = range(6)

#buyer information
date = ""
time = ""
location = ""
amount = ""
meal = ""
contact = ""
reply = ""

#seller information
sellerDate = ""
sellerTime = ""
sellerLocation = ""
sellerAmount = ""
sellerMeal = ""
sellerContact = ""

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def pullFromBackend():
    global result

    result = app.get('/Coupon', None)
    print(result)

    # print("***")
    # print(result['-LWaKLCQoFzjTRgnflJj'])
    # print("***")

pullFromBackend()

def start(bot, update):
    reply_keyboard = [['Breakfast', 'Dinner']]

    print('START')

    update.message.reply_text(
        'Hi there! Welcome to FoodExchange, '
                     'a bot that helps you buy meal credits. '
                     'Try the /help '
                     'command to see all available commands.' 
                     '\n'
                     'What meal would you like to purchase? Each meal costs $2.50.\n'
                     'You can view the menu today at @rcmealbot',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MEAL

def cancel(bot, update):
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def meal(bot, update):
    global meal
    reply_keyboard = [['Today\n', 'Tomorrow\n', 'Day After Tomorrow\n']]
    user = update.message.from_user

    logger.info("%s has selected breakfast/dinner: %s", user.first_name, update.message.text)

    update.message.reply_text('I see! I have noted your choice. Now when would you like to purchase this meal?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    meal = update.message.text

    print(meal)

    return DATE

def date(bot, update):
    global date 

    user = update.message.from_user

    reply_keyboard_am = [['07:00 - 08:00\n', '08:00 - 09:00\n','09:00 - 10:00\n']]
    reply_keyboard_pm = [['17:00 - 18:00\n', '18:00 - 19:00\n','19:00 - 20:00\n']]

    logger.info("%s has chosen date: %s", user.first_name, update.message.text)

    if update.message.text == 'Today':
        date = "2019-01-20"
    elif update.message.text == 'Tomorrow':
        date = "2019-01-21"
    else:
        date = "2019-01-22"

    if meal == 'Breakfast':
        reply_keyboard = reply_keyboard_am
    else:
        reply_keyboard = reply_keyboard_pm

    update.message.reply_text('Excellent. Now, please tell me what time you would like to purchase the meal credit?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    #date = update.message.text

    print(date)

    return TIME

def time(bot, update):
    global time

    user = update.message.from_user
    reply_keyboard = [['Cinnamon / Tembusu Dining Hall\n', 'Capt / RC4 Dining Hall\n']]

    logger.info("%s has chosen the following time: %s", user.first_name, update.message.text)

    update.message.reply_text('I see! Now please chose your location.',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    time = update.message.text

    print(time)

    return LOCATION

def location(bot, update):
    global location

    user = update.message.from_user

    logger.info("%s has selected the location: %s", user.first_name, update.message.text)

    update.message.reply_text('I see! I have noted your contact information. I am now trying to match you with the most suitable seller ...')

    location = update.message.text

    print(location)

    matchBuyerToSeller(bot,update)

# def amount(bot, update):
#     global amount

#     user = update.message.from_user

#     logger.info("%s has selected the amount: %s", user.first_name, update.message.text)

#     update.message.reply_text('I see! I have noted your choice. Now please give me your telegram handle')

#     amount = update.message.text

#     print(amount)

#     return CONTACT

def pushToBackend(userID):

    # data = {
    #   "amount" : "amount",
    #   "date" : "date",
    #   "location" : "location",
    #   "mealType" : "meal",
    #   "telegramHandle" : "contact",
    #   "time" : "time"

    # }

    #result = app.get('/Coupon', None)

    result = app.put("Coupon/" + userID ,"soldStatus", "pending")

   # usersRef.child(userID).set("pending")

    #result = app.post('/Coupon/' + userID, data)

    print("This is the result of pushing and the userID")
    print(userID)
    print(result)

# def contact(bot, update):
#     global contact 

#     user = update.message.from_user

#     logger.info("%s contact is: %s", user.first_name, update.message.text)

#     update.message.reply_text('I see! I have noted your contact information. I am now trying to match you with the most suitable seller ...')

#     contact = update.message.text

#     print(contact)

#     print("matching buyer to seller")

#     matchBuyerToSeller(bot,update)

def matchBuyerToSeller(bot, update):

    user = update.message.from_user

    print("PRINTING RESULT")
    print(result)
    print("PRINTING RESULT")

    print(result.keys())

    # for value in result.values():
    #     if meal == (result[meal])
    #         print("true")

    print("PERSON IS PRINTING")
    print(result)
    for (person, key) in zip(result.values(), result.keys()):
        print(person)

        if person['soldStatus'] == 'false' and person['mealType'] == meal and person['date'] == date and person['time'] == time:
            if person['location'] == location:
                print(person['telegramHandle'])
                update.message.reply_text('Hurray! We have found you a seller. Please contact ' + (person['telegramHandle']) + ' for your meal credit')
                pushToBackend(key)
                return
            else:
                print(location, person['location'])
                update.message.reply_text('We did not manage to find someone at ' + location + ' but there is someone at ' + person['location'] + '! Contact them at ' + (person['telegramHandle']))
                pushToBackend(key)
                return

    print(meal, date, time)

    update.message.reply_text('No sellers are available at the moment, press /retry to retry again')

def retry(bot, update):

    if location == "":
        update.message.reply_text('You have not filled in the required fields. Press /start or continue filling in the information required.')
        return

    print("calling RETRY function now")

    user = update.message.from_user

    pullFromBackend()

    reply = update.message.text

    print(reply)
    
    matchBuyerToSeller(bot, update)

    """
    {'-LWaKLCQoFzjTRgnflJj': {'amount': 'amount', 'date': 'date', 
    'location': 'location', 'mealType': 'meal', 'telegramHandle': 'contact', 'time': 'time'}, 
    '-LWaMi7D1H97CG-VPgZg': {'amount': 'Capt/RC4 Dining Hall', 'date': 'Breakfast', 
    'location': '7-8', 'mealType': '/start', 'telegramHandle': 'dhsjkhsk', 'time': 'Tomorrow'}, 
    '-LWaOW86GA35QwYUQbwU': {'amount': 'Cinnamon/Tembusu Dining Hall', 'date': 'Breakfast', 
    'location': '9-10', 'mealType': '/start', 'telegramHandle': '10', 'time': 'Today'}, 
    '-LWaQO46kq5VnLBy7nWT': {'amount': '1', 'date': 'Today', 
    'location': 'Cinnamon/Tembusu Dining Hall', 'mealType': 'Breakfast', 'telegramHandle': 'djhsjkhdjks', 'time': '7-8'}, 'exampleId': {'amount': 1, 'date': '2019-01-19', 'location': 'Cinnamon Collage', 'mealType': 'Breakfast', 'soldStatus': False, 'telegramHandle': '@CalvinTantio', 'time': '15:00'}}
    """

def help(bot, update):
    help_message = ('You can control me by sending these commands:\n'
                    '/buy - buy a meal credit from someone\n'
                    '/menu - view the menu today'
                    )

    update.message.reply_text(help_message)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    #dp.add_handler(CommandHandler('create', create))
    #dp.add_handler(CommandHandler('tweet', tweet))
    #updater.dispatcher.add_handler(CallbackQueryHandler(confirm_tweet))
    #dp.add_handler(CommandHandler('saved', saved))
    #dp.add_handler(MessageHandler(Filters.text, create_tweet))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('retry', retry)],

        states={

            MEAL: [RegexHandler('^(Breakfast|Dinner)$', meal), CommandHandler('retry', retry)],

            DATE: [RegexHandler('^(Today|Tomorrow|Day After Tomorrow)$', date), CommandHandler('retry', retry)],

            TIME: [RegexHandler('^(07:00 - 08:00|08:00 - 09:00|09:00 - 10:00|17:00 - 18:00|18:00 - 19:00|19:00 - 20:00)$', time), CommandHandler('retry', retry)],

            LOCATION: [RegexHandler('^(Cinnamon / Tembusu Dining Hall|Capt / RC4 Dining Hall)$', location), CommandHandler('retry', retry)]

            #RETRY: [RegexHandler('^(Retry)$', retry)]

            #AMOUNT: [MessageHandler(Filters.text, amount)],

            #CONTACT: [MessageHandler(Filters.text, contact)]

            #BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

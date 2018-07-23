import re
import datetime
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import urllib.parse

#Enable Logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
#Take todays date
def month():
    now = datetime.datetime.now()
    month = now.strftime("%B")
    month = month.lower()
    return month
def day():
    now = datetime.datetime.now()
    day = now.strftime("%d")
    return day

#create bbc-link

def get_url():
    url = 'http://news.bbc.co.uk/onthisday/low/dates/stories/'+month()+'/'+day()+'/default.stm'
    return url

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

def get_request():
    req = urllib.request.Request(get_url(), headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    return respData


#Parse on-this-day BBC-Link
#values = {'s':'basics','submit':'search'}

#data = urllib.parse.urlencode(values)
'''
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
respData = resp.read
print(respData)
'''

'''
try:
    url = 'http://news.bbc.co.uk/onthisday/low/dates/stories/'+month()+'/'+day()+'/default.stm'

    # now, with the below headers, we defined ourselves as a simpleton who is
    # still using internet explorer.
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

except Exception as e:
    print(str(e))
'''
i = 0
titles = re.findall(r'<span class="h1">(.*?)</span>',str(get_request()))
explanations = re.findall(r'<br>(.*?)<br clear="ALL">',str(get_request()))
exp=[]
A =[]

for eachE in explanations:
    eachE = eachE[14:len(eachE)]
    exp.append(eachE)
while i < len(titles)-1:
    news= titles[i]+ ': ' + exp[i]
    A.append(news)
    i+=1
print(A)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Welcome to On-this-Day-Bot! We send todays historical events of the day! If you want to see them now, just type "/today" ')


def today(bot, update):
    """Send a message when the command /today is issued."""
    for eachA in A:
        update.message.reply_text(eachA)
    update.message.reply_text('Source: '+str(get_url()))
    

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text('Welcome to On-this-Day-Bot! We send todays historical events of the day! If you want to see them now, just type "/today" ')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("YOUR BOT TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()




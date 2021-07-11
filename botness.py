from os import getenv
from telegram import Bot
from telegram.ext import Dispatcher
from handlers import *
import tweepy
from deta import Deta

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
TWITTER_KEY = getenv('TWITTER_KEY')
TWITTER_SECRET = getenv("TWITTER_ENV")
DETA_PROJECT_KEY = getenv("DETA_PROJECT_KEY")

deta = Deta(DETA_PROJECT_KEY)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, None, workers=0)

# Register handlers
dp.add_handler(start_cmd_handler)
dp.add_handler(tweet_cmd_handler)
dp.add_handler(help_cmd_handler)
dp.add_handler(edits_handler)
dp.add_handler(attachment_handler)
dp.add_handler(unrecognized_hanlder)
dp.add_error_handler(error_handler)
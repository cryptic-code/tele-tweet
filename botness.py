from os import getenv
from telegram import Bot
from telegram.ext import Dispatcher, Defaults, ExtBot
from update_handlers import *

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

defaults = Defaults(parse_mode='markdown')
bot = ExtBot(token=TELEGRAM_TOKEN, defaults=defaults)
dp = Dispatcher(bot, None, workers=0)

# Register handlers
dp.add_handler(start_cmd_handler)
dp.add_handler(help_cmd_handler)
dp.add_handler(auth_cmd_handler)
dp.add_handler(verify_cmd_handler)
dp.add_handler(tweet_cmd_handler)
dp.add_handler(edits_handler)
dp.add_handler(attachment_handler)
dp.add_handler(tweet_handler)
dp.add_handler(scan_tweet_handler)
dp.add_handler(unrecognized_hanlder)
dp.add_error_handler(error_handler)

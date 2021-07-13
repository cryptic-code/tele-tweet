from os import getenv
from telegram.ext import Dispatcher, Defaults, ExtBot
from telegram import BotCommand
from update_handlers import *

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')

defaults = Defaults(disable_web_page_preview=True)
bot = ExtBot(token=TELEGRAM_TOKEN, defaults=defaults)
dp = Dispatcher(bot, None, workers=0)

# Register handlers
dp.add_handler(start_cmd_handler)
dp.add_handler(help_cmd_handler)
dp.add_handler(auth_cmd_handler)
dp.add_handler(verify_cmd_handler)
dp.add_handler(tweet_cmd_handler)
dp.add_handler(stats_cmd_handler)
dp.add_handler(samples_cmd_handler)
dp.add_handler(edits_handler)
dp.add_handler(attachment_handler)
dp.add_handler(tweet_handler)
dp.add_handler(scan_handler)
dp.add_handler(unrecognized_hanlder)
dp.add_error_handler(error_handler)

# Define commands
def set_bot_commands():
    help_cmd = BotCommand('help', 'Get help on using the bot.')
    stats_cmd = BotCommand('stats', 'See your tweeting stats.')
    auth_cmd = BotCommand('auth', "Authorize the bot with Twitter account.")
    samples_cmd = BotCommand('samples', "Sample msgs to understand syntax.")

    commands = (help_cmd, stats_cmd, auth_cmd, samples_cmd)

    bot.set_my_commands(commands=commands)
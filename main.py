from os import getenv
from custom_logging import get_logger
from botness import bot, dp, set_bot_commands
from telegram import Update
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

APP_URL = getenv('APP_URL')
ADMIN_PASS = getenv('ADMIN_PASS')

pass_header = 'Passkey'
webhook_endpoint = '/tele-tweet'

logger = get_logger(__name__, only_debug=True)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route(webhook_endpoint, methods=["POST", "GET"])
def handle_update():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dp.process_update(update)
        return "OK"
    else:
        return "Hello, world! ;)"

@app.route('/set-commands')
def set_commands():
    try:
        if request.headers[pass_header] == ADMIN_PASS:
            set_bot_commands()
            return "Commands Set"
    except:
        return "Eh!"

@app.route('/set-webhook')
def set_webhook_handler():
    try:
        if request.headers[pass_header] == ADMIN_PASS:
            bot.set_webhook(url=APP_URL+webhook_endpoint)
            return "Webhook Set"
    except:
        return "Eh!"

@app.route('/delete-webhook')
def delete_webhook_handler():
    try:
        if request.header[pass_header] == ADMIN_PASS:
            bot.delete_webhook(drop_pending_updates=True)
            return "Webhook Deleted"
    except:
        return "Eh!"
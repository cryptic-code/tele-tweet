from os import getenv
from read_config import get_reply
from twitter_inetractions import authorize, create_auth_url, post_tweets, validate_tweets
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters
from deta import Deta

DETA_PROJECT_KEY = getenv("DETA_PROJECT_KEY")

deta = Deta(DETA_PROJECT_KEY)

chats_db = deta.Base("chats")
cred_db = deta.Base("tw_cred")

def error_handler(update: Update, context: CallbackContext) -> None:
    """ Handle application errors. """

    reply = get_reply("App_err")
    context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

def handle_validity_response(response: dict, is_thread: bool) -> str:
    """ Read the response dictionary and return the reply. """

    if response["error"]:
        if is_thread:
            reply = get_reply('Tweet_thread_lengthy', msg_index=response['msg_index'], msg_len=response['msg_len'])
        elif not is_thread:
            reply = get_reply('Tweet_lengthy', msg_len=response['msg_len'])
    else:
        reply = None

    return reply

class CommandCallbacks():
    def __init__(self) -> None:
        pass

    @staticmethod
    def start_cmd_handler(update: Update, context: CallbackContext) -> None:
        """ Handle `/start` command. """

        chat_id = update.effective_message.chat_id
        sender_first_name = update.message.from_user.first_name
        record = chats_db.get(key=str(chat_id))
        if record:
            reply = get_reply('Start_cmd_welcome', first_name=sender_first_name)
        else:
            chats_db.put({'tweet_count': 0}, key=str(chat_id))
            reply = get_reply('Start_cmd', first_name=sender_first_name)
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

    @staticmethod
    def help_cmd_handler(update: Update, context: CallbackContext) -> None:
        """ Handle `/help` command. """

        sender_first_name = update.message.from_user.first_name
        reply = get_reply('Help_cmd', first_name=sender_first_name)

        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

    @staticmethod
    def tweet_cmd_handler(update: Update, context: CallbackContext) -> None:
        """ Handle `/tweet` commmand. """

        reply = get_reply('Tweet_cmd')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)
    
    @staticmethod
    def auth_cmd_handler(update: Update, context: CallbackContext) -> None:
        """ Handle `/auth` command. """
        
        chat_id = update.effective_message.chat_id
        auth_url, req_token = create_auth_url()

        cred_db.put({'req_token': req_token}, key=str(chat_id))

        reply = get_reply('Auth_instructions', auth_url=auth_url)
        context.bot.send_message(chat_id=chat_id, text=reply)

    @staticmethod
    def verify_cmd_hanlder(update: Update, context: CallbackContext) -> None:
        """ Handle `/verify` command. """

        chat_id = update.effective_message.chat_id
        record = cred_db.get(key=str(chat_id))
        verifier = context.args[0]

        auth = authorize(record['req_token'], verifier)

        if auth:
            cred_db.put(auth, key=str(chat_id))
            reply = get_reply('Auth_success')
        else:
            reply = get_reply('Auth_err')

        context.bot.send_message(chat_id=chat_id, text=reply)

    @staticmethod
    def stats_cmd_handler(update: Update, context: CallbackContext) -> None:
        """ Handle `/stats` command."""

        chat_id = update.effective_message.chat_id
        record = chats_db.get(str(chat_id))

        reply = get_reply('Stats_cmd', tweet_count=record['tweet_count'])

        context.bot.send_message(chat_id=chat_id, text=reply)

class MessageCallbacks():
    def __init__(self) -> None:
        pass

    @staticmethod
    def edits_handler(update: Update, context: CallbackContext) -> None:
        """ Handle edited messages. """

        reply = get_reply('EDIT_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

    @staticmethod
    def unrecognized_handler(update: Update, context: CallbackContext) -> None:
        """ Handle unrecognized messages. """

        reply = get_reply('UNRECOGNIZED_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

    @staticmethod
    def attachment_handler(update: Update, context: CallbackContext) -> None:
        """ Handle attachments. """
        
        reply = get_reply('ATTACHMENT_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply)

    @staticmethod
    def tweet_handler(update: Update, context: CallbackContext):
        """ Reply with the link to the tweet sent. """

        chat_id = update.effective_message.chat_id
        auth = cred_db.get(str(chat_id))

        msg_txt = update.effective_message.text
        tweets = msg_txt.split('\n\n///\n\n')

        if len(tweets) > 1:
            is_thread = True
        else:
            is_thread = False

        response = validate_tweets(tweets)
        reply = handle_validity_response(response, is_thread)

        if not reply:
            response = post_tweets(auth, tweets)

            if response["error"]:
                reply = get_reply("Tweet_err")
            elif is_thread:
                reply = get_reply("Tweet_thread_success", tweet_url=response['tweet_url'])
            else:
                reply = get_reply("Tweet_sucess", tweet_url=response['tweet_url'])

            record = chats_db.get(str(chat_id))
            record['tweet_count']+=response['tweet_coutnt']
            chats_db.put(record, key=str(chat_id))

        context.bot.send_message(chat_id=chat_id, text=reply)

    @staticmethod
    def scan_tweet_handler(update: Update, context: CallbackContext) -> None:
        """ Send the status if the received tweet(s) is within character limit. """

        msg_txt = update.effective_message.text
        tweets = msg_txt.split('\n\n///\n\n')

        response = validate_tweets(tweets)
        reply = handle_validity_response(response)

        context.bot.send_message(chat_id=update.message.chat_id, text=reply)

# Command Handlers
start_cmd_handler = CommandHandler(command='start', callback=CommandCallbacks.start_cmd, filters=(~Filters.update.edited_message))

help_cmd_handler = CommandHandler(command='help', callback=CommandCallbacks.help_cmd, filters=(~Filters.update.edited_message))

auth_cmd_handler = CommandHandler(command='auth', callback=CommandCallbacks.auth_cmd_handler, filters=(~Filters.update.edited_message))

verify_cmd_handler = CommandHandler(command='verify', callback=CommandCallbacks.verify_cmd_hanlder, filters=(~Filters.update.edited_message))

tweet_cmd_handler = CommandHandler(command='tweet', callback=CommandCallbacks.tweet_cmd, filters=(~Filters.update.edited_message))

# Message Handlers
edits_handler = MessageHandler(filters=(Filters.update.edited_message), callback=MessageCallbacks.edits_handler)

attachment_handler = MessageHandler(filters=(Filters.attachment), callback=MessageCallbacks.attachment_handler)

tweet_handler = MessageHandler(filters=(Filters.text & Filters.regex('^tweet\n\n|^Tweet\n\n') &~ Filters.update.edited_message), callback=MessageCallbacks.tweet_handler)

scan_tweet_handler = MessageHandler(filters=(Filters.text & Filters.regex('^scan\n\n|^Scan\n\n') &~ Filters.update.edited_message), callback=MessageCallbacks.scan_tweet_handler)

unrecognized_hanlder = MessageHandler(filters=(Filters.text &~ Filters.update.edited_message), callback=MessageCallbacks.unrecognized_handler)

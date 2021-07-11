from read_config import get_reply
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters

class CommandCallbacks():
    def __init__(self) -> None:
        pass

    @classmethod
    def start_cmd(cls, update: Update, context: CallbackContext) -> None:
        """ Handle `/start` command. """

        reply = get_reply('START_CMD')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

    @classmethod
    def help_cmd(cls, update: Update, context: CallbackContext) -> None:
        """ Handle /help command. """

        reply = get_reply('HELP_CMD')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

    @classmethod
    def tweet_cmd(cls, update: Update, context: CallbackContext) -> None:
        """ Handle `/tweet` commmand. """

        reply = get_reply('TWEET_CMD')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

class MessageCallbacks():
    def __init__(self) -> None:
        pass

    @classmethod
    def edits_reply(cls, update: Update, context: CallbackContext) -> None:
        """ Handle edited messages. """

        reply = get_reply('EDIT_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

    @classmethod
    def unrecongnized_reply(cls, update: Update, context: CallbackContext) -> None:
        """ Handle unrecognized messages. """

        reply = get_reply('UNRECOGNIZED_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

    @classmethod
    def attachment_reply(cls, update: Update, context: CallbackContext) -> None:
        """ Handle attachments. """
        
        reply = get_reply('ATTACHMENT_ERR')
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=reply, parse_mode='markdown')

def error_handler(update: Update, context: CallbackContext) -> None:
    """ Handle application errors. """

    context.bot.send_message(chat_id=update.effective_message.chat_id, text=get_reply('APP_ERR'), parse_mode='markdown')


# def tweet_send_handler(update: Update, context: CallbackContext):
#     """ Handle sending out a single tweet. """
#     auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
#     auth.set_access_token()

# Command Handlers
start_cmd_handler = CommandHandler(command='start', callback=CommandCallbacks.start_cmd, filters=(~Filters.update.edited_message))
help_cmd_handler = CommandHandler(command='help', callback=CommandCallbacks.help_cmd, filters=(~Filters.update.edited_message))
tweet_cmd_handler = CommandHandler(command='tweet', callback=CommandCallbacks.tweet_cmd, filters=(~Filters.update.edited_message))

# Message Handlers
edits_handler = MessageHandler(filters=(Filters.update.edited_message), callback=MessageCallbacks.reply_edits)
attachment_handler = MessageHandler(filters=(Filters.attachment), callback=MessageCallbacks.attachment_reply)
unrecognized_hanlder = MessageHandler(filters=(Filters.text &~ Filters.update.edited_message &~ Filters.command &~ Filters.regex('^define.|^Define.')), callback=MessageCallbacks.unrecongnized_reply)
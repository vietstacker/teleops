"""Echo plugin.

/echo - Do nothing!
"""


def handle(bot, update):
    """I am Meditech Bot."""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Hey! I\'m Meditech Bot')

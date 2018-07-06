"""Show Meditech."""
from telebot import emojies


def handle(bot, update):
    """Meditech says hello."""
    msg = '{0} Meditech JSC {1}' . format(emojies.fire, emojies.fire)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)

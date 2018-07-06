import configparser

from telebot import bot


def get_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def main(args):
    config = get_config(args.config_file)
    BOT = bot.Bot(config['DEFAULT']['telegram_token'])
    BOT.run()
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    BOT.idle()

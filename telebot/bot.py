import importlib
import logging
import os
import pkgutil
import sys
import traceback

import telebot.plugins

from telebot import emojies
from telebot import settings

from telebot.plugins import create

from telegram.ext import ConversationHandler
from telegram.ext import callbackqueryhandler
from telegram.ext import CommandHandler
from telegram.ext import Updater

LOG = logging.getLogger(__name__)


def strip_extension(lst):
    return (os.path.splitext(l)[0] for l in lst)


class Bot(object):
    """Bot class."""

    def __init__(self, token):
        self.scheduler = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.plugins = {}
        self.plugin_modules = []
        self.init_handlers()

    def init_handlers(self):
        """Init all command handlers."""
        self.init_plugins()
        # Init general command handlers
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(help_handler)
        # Init additional plugins handlers
        for plugin in self.plugins.keys():
            if plugin in settings.Continue_PLUGINS:
                continue
            elif plugin in settings.ARGS_PLUGINS:
                _handler = CommandHandler(plugin,
                                          self.plugins[plugin]['handler'],
                                          pass_args=True)
            elif plugin in settings.JOB_PLUGINS:
                _handler = CommandHandler(plugin,
                                          self.plugins[plugin]['handler'],
                                          pass_args=True,
                                          pass_job_queue=True,
                                          pass_chat_data=True)
            elif plugin in settings.CONV_PLUGINS:
                module = importlib.import_module('telebot.plugins.' + plugin)
                _handler = module.conv_handler
            elif plugin in settings.NORMAL_PLUGINS:
                _handler = CommandHandler(plugin,
                                          self.plugins[plugin]['handler'])
            else:
                _handler = None
            if _handler:
                self.dispatcher.add_handler(_handler)
        self.dispatcher.add_error_handler(self.error)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        LOG.warning('Update "%s" caused error "%s"', update, error)

    def _get_commands(self):
        commands = []
        all_plugins = (settings.NORMAL_PLUGINS + settings.CONV_PLUGINS +
                       settings.JOB_PLUGINS)
        for name, helper in self.plugins.items():
            if name in all_plugins:
                command = '/' + name
                whatis = helper['whatis']
                commands.append([command, whatis])
            else:
                continue
        return commands

    def run(self):
        self.updater.start_polling(clean=True)
        return

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hello! Meditech bot is ready. Please enter '
                              '/help to show all command that will help you.')

    def stop(self):
        self.updater.stop()
        return

    def idle(self):
        self.updater.idle()
        return

    def help(self, bot, update):
        commands = self._get_commands()
        command_names = [cmd[0].strip('/') for cmd in commands]

        text = 'Please type: /help <command> with <command> is optional.'
        user_input = update.message.text.split(' ')
        if len(user_input) == 1:
            text = emojies.information_source + \
                   ' The following commands are available:\n'

            for command in commands:
                text += command[0] + '-' + command[1] + '\n'
        elif len(user_input) == 2 and user_input[1] in command_names:
            text = emojies.information_source + ' ' + \
                   self.plugins[user_input[1]]['usage']

        bot.send_message(chat_id=update.message.chat_id, text=text)

    def init_plugins(self):
        for _, name, _ in pkgutil.iter_modules(telebot.plugins.__path__):
            if name in settings.JOB_PLUGINS or name in settings.NORMAL_PLUGINS \
                    or name in settings.CONV_PLUGINS \
                    or name in settings.ARGS_PLUGINS:
                try:
                    LOG.debug('Plugin: {}'.format(name))
                    module = importlib.import_module('telebot.plugins.' + name)
                    module_name = module.__name__.split('.')[-1]
                    _info = {
                        'whatis': 'Unknown command',
                        'usage': 'Unknown usage',
                        'handler': getattr(module, 'handle')
                    }

                    if module.__doc__:
                        _info['whatis'] = module.__doc__.split('\n')[0]
                        _info['usage'] = module.__doc__
                    LOG.info(_info)
                    self.plugins[module_name] = _info
                except Exception:
                    LOG.warning('Import failed on module {}, module not loaded!'.
                                format(name))
                    LOG.warning('{}'.format(sys.exc_info()[0]))
                    LOG.warning('{}'.format(traceback.format_exc()))

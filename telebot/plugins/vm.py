from telebot.plugins import novautils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler,\
    ConversationHandler, RegexHandler, MessageHandler, Filters


CHOOSING = range(1)


def handle(bot, update):
    query = update.callback_query
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    list_servers = []
    keyboard_servers = []
    dict_servers = nov.list_vm()
    #print(dict_servers)
    for dict_server in dict_servers:
        list_servers.append(dict_server)
    #print(list_servers)
    for list_server in list_servers:
        keyboard_servers.append(InlineKeyboardButton
                                (list_server,
                                 callback_data='name_vm' + '_' + list_server))
    #print(keyboard_servers)
    reply_markup = InlineKeyboardMarkup([keyboard_servers])
    update.message.reply_text(u"List VM",
                              reply_markup=reply_markup)
    # bot.edit_message_reply_markup(
    #     chat_id=query.message.chat_id,
    #     message_id=query.message.message_id,
    #     reply_markup=reply_markup)
    return CHOOSING


def menu_detail_vm(bot, update):
    query = update.callback_query
    query_data = update.callback_query.data
    name_vm = query_data[8:]
    #print(name_vm)
    keyboard = [[InlineKeyboardButton("status", callback_data='status_' + name_vm ),
                 InlineKeyboardButton("stop", callback_data='stop_' + name_vm)],
                [InlineKeyboardButton("start", callback_data='start_' + name_vm)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text(
    #     u"Press option",
    #     reply_markup=reply_markup
    # )
    bot.edit_message_text(text='Options:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def status_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    name_vm = query_data[7:]
    # print(name_vm)
    dict_servers = nov.list_vm()
    status = dict_servers[name_vm]
    # print(status)
    # reply_markup = InlineKeyboardMarkup([InlineKeyboardButton(status, callback_data='minhkma')])
    keyboard = [InlineKeyboardButton(str(status), callback_data='status')]
    reply_markup = InlineKeyboardMarkup([keyboard])
    bot.edit_message_text(text='status {0}'.format(name_vm),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def stop_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    # print('stop {}'.format(query_data))
    name_vm = query_data[5:]
    print(name_vm)
    nov.control(name_vm=name_vm, action_vm='stop')
    bot.edit_message_text(text='oke',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def start_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    # print('start {}'.format(query_data))
    name_vm = query_data[6:]
    # print(name_vm)
    nov.control(name_vm=name_vm, action_vm='start')
    bot.edit_message_text(text='oke',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def choose(bot, update):
    query = update.callback_query
    query_data = query.data
    # print(query_data)
    if query_data.startswith('name_vm_'):
        menu_detail_vm(bot, update)
        # return CHOOSING
    elif query_data.startswith('status_'):
        status_vm(bot, query)
        # return CHOOSING
    elif query_data.startswith('stop_'):
        stop_vm(bot, query)
        # return CHOOSING
    elif query_data.startswith('start_'):
        start_vm(bot, query)


def close(bot, query):
    bot.edit_message_text(text='Bye bye baby',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('vm', handle)],
    states={
    CHOOSING: [CallbackQueryHandler(choose)]
    },
    fallbacks=[CommandHandler('vm', handle)]
)

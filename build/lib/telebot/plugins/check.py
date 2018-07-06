from telebot.plugins import novautils
from  telebot.plugins import networkutils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler,\
    ConversationHandler, RegexHandler, MessageHandler, Filters

CHOOSING = range(1)


def convert_keyboard_inline(list_items):
    # list_items = []
    # keyboard_items = []
    # for dict_item in dict_items:
    #     row = []
    #     row.extend([dict_item, dict_items[dict_item]])
    #     list_items.append(row)
    keyboard_items = []
    for list_item in list_items:
        keyboard_row = []
        for count,_item in enumerate(list_item):
            keyboard_row.append(InlineKeyboardButton(list_item[count],
                                                 callback_data='minh'))
        keyboard_items.append(keyboard_row)
    reply_markup = InlineKeyboardMarkup(keyboard_items)
    return reply_markup


def handle(bot, update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("check nova",
                                      callback_data='nova'),
                 InlineKeyboardButton("check neutron",
                                      callback_data='neutron')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(u"Select option",
                              reply_markup=reply_markup)
    # bot.edit_message_reply_markup(
    #     chat_id=query.message.chat_id,
    #     message_id=query.message.message_id,
    #     reply_markup=reply_markup)
    return CHOOSING


def choose(bot, update):
    query = update.callback_query
    query_data = query.data
    if query_data == 'nova':
        check_nova(bot, update)
    elif query_data == 'neutron':
        check_neutron(bot, update)


def check_nova(bot, update):
    query = update.callback_query
    query_data = query.data
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    # neu = networkutils.Neutron('192.168.100.114', 'admin', 'locdev', 'admin')
    list_services = nov.service()
    msg = convert_keyboard_inline(list_services)
    # update.message.reply_text("Agent Nova",
    #                               reply_markup=msg)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=msg)

def check_neutron(bot, update):
    query = update.callback_query
    query_data = query.data
    neu = networkutils.Neutron('192.168.100.114', 'admin', 'locdev', 'admin')
    dict_services = neu.list_agent()
    list_services = []
    for dict_service in dict_services:
        list_service = []
        # print(dict_service)
        list_service.extend([dict_service['agent_type'],
                            dict_service['host'],
                            str(dict_service['alive'])])
        list_services.append(list_service)
    # print(list_services)
    msg = convert_keyboard_inline(list_services)
    # print(msg)
    # update.message.reply_text("Agent Neutron",
    #                            reply_markup=msg)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=msg)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('check', handle)],
    states={
    CHOOSING: [CallbackQueryHandler(choose)]
    },
    fallbacks=[CommandHandler('check', handle)]
)
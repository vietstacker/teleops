from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.plugins import novautils
from  telebot.plugins import networkutils
from telegram.ext import CommandHandler, CallbackQueryHandler,\
    ConversationHandler, RegexHandler, MessageHandler, Filters


CHOOSING, FIRST, SECOND, THIRD, FOURTH, FIFTH  = range(6)
data = {}


def handle(bot, update):
    keyboard = [[InlineKeyboardButton("Check agent",
                                      callback_data='check'),
                 InlineKeyboardButton("VM detail",
                                      callback_data='vm')],
                [InlineKeyboardButton("Create VM", callback_data='create')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(u"Select option",
                              reply_markup=reply_markup)
    return CHOOSING


def choose(bot, update):
    query = update.callback_query
    query_data = query.data
    print(query_data)
    if query_data == 'vm':
        vm(bot, update)
    elif query_data.startswith('name_vm_'):
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
    elif query_data == 'check':
        check(bot, update)
    elif query_data == 'nova':
        check_nova(bot, update)
    elif query_data == 'neutron':
        check_neutron(bot, update)
    elif query_data == 'create':
        create_vm(bot, update)
        return FIRST
    elif query_data == 'back_page_1':
        back_page_1(bot, update)
    elif query_data == 'back_page_2_vm':
        vm(bot, update)
    elif query_data.startswith('delete_'):
        delete_vm(bot, query)


def vm(bot, update):
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
    print(keyboard_servers)
    keyboard_servers.append(InlineKeyboardButton('<< Back',
                                                  callback_data='back_page_1'))
    reply_markup = InlineKeyboardMarkup([keyboard_servers])
    # update.message.reply_text(u"List VM",
    #                           reply_markup=reply_markup)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return CHOOSING


def menu_detail_vm(bot, update):
    query = update.callback_query
    query_data = update.callback_query.data
    name_vm = query_data[8:]
    #print(name_vm)
    keyboard = [[InlineKeyboardButton("status", callback_data='status_' + name_vm ),
                 InlineKeyboardButton("stop", callback_data='stop_' + name_vm),
                 InlineKeyboardButton("delete", callback_data='delete_'+ name_vm)],
                [InlineKeyboardButton("start", callback_data='start_' + name_vm),
                 InlineKeyboardButton("<< Back", callback_data='back_page_2_vm')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text(
    #     u"Press option",
    #     reply_markup=reply_markup
    # )
    bot.edit_message_text(text='Options:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return CHOOSING


def stop_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    # print('stop {}'.format(query_data))
    name_vm = query_data[5:]
    print(name_vm)
    nov.control(name_vm=name_vm, action_vm='stop')
    keyboard = [InlineKeyboardButton('<< Back',
                                          callback_data='back_page_2_vm')]
    reply_markup = InlineKeyboardMarkup([keyboard])
    bot.edit_message_text(text='oke',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return CHOOSING


def start_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    # print('start {}'.format(query_data))
    name_vm = query_data[6:]
    # print(name_vm)
    nov.control(name_vm=name_vm, action_vm='start')
    keyboard = [InlineKeyboardButton('<< Back',
                                          callback_data='back_page_2_vm')]
    reply_markup = InlineKeyboardMarkup([keyboard])
    bot.edit_message_text(text='oke',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return CHOOSING


def delete_vm(bot, query):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query_data = query.data
    # print('start {}'.format(query_data))
    name_vm = query_data[7:]
    print(name_vm)
    nov.control(name_vm=str(name_vm), action_vm='delete')
    keyboard = [InlineKeyboardButton('<< Back',
                                          callback_data='back_page_2_vm')]
    reply_markup = InlineKeyboardMarkup([keyboard])
    bot.edit_message_text(text='oke',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return CHOOSING


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
    keyboard.append(InlineKeyboardButton('<< Back',
                                          callback_data='back_page_2_vm'))
    reply_markup = InlineKeyboardMarkup([keyboard])
    bot.edit_message_text(text='status {0}'.format(name_vm),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return CHOOSING


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
    keyboard_items.append([InlineKeyboardButton('<< Back',
                                                callback_data='back_page_1')])
    reply_markup = InlineKeyboardMarkup(keyboard_items)
    return reply_markup


def check(bot, update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("check nova",
                                      callback_data='nova'),
                 InlineKeyboardButton("check neutron",
                                      callback_data='neutron')]]
    keyboard.append([InlineKeyboardButton('<< Back',
                                         callback_data='back_page_1')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text(u"Select option",
    #                           reply_markup=reply_markup)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return CHOOSING


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


def create_vm(bot, update):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(u"Network", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    print(type(reply_markup))
    # update.message.reply_text(
    #     u"Press network",
    #     reply_markup=reply_markup
    # )
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return FIRST


def first(bot, update):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query = update.callback_query
    dict_networks = nov.networks()
    print(dict_networks)
    keyboard_networks = nov.keybroad_items(dict_networks)
    print(query.data)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"Select network")
    reply_markup = InlineKeyboardMarkup(keyboard_networks)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    # print(query.data)
    return SECOND


def second(bot, update):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query = update.callback_query
    data["network"] = query.data
    dict_images = nov.list_images()
    keyboard_images = nov.keybroad_items(dict_images)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"select image"
    )
    reply_markup = InlineKeyboardMarkup(keyboard_images)
    print('abc : {0}'.format(reply_markup))
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return THIRD


def third(bot, update):
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    query = update.callback_query
    data["image"] = query.data
    dict_flavors = nov.list_flavors()
    keyboard_flavors = nov.keybroad_items(dict_flavors)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"select flavor"
    )
    reply_markup = InlineKeyboardMarkup(keyboard_flavors)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return FOURTH


def choose_name(bot, update):
    query = update.callback_query
    data['flavor'] = query.data
    update.callback_query.message.reply_text(
        "Alright, a new VM. Please choose a name for your VM.")
    return FIFTH


def name(bot, update):
    query = update.callback_query
    name_vm = update.message.text
    # data['flavor'] = update.callback_query.data
    data['name'] = name_vm
    print(data)
    nov = novautils.Nova('192.168.100.114', 'admin', 'locdev', 'admin')
    nov.create_vm(name= data['name'],
                  image= data['image'],
                  flavor= data['flavor'],
                  nic= data['network'])
    # keyboard = [InlineKeyboardButton('<< Back',
    #                                       callback_data='back_page_2_vm')]
    # reply_markup = InlineKeyboardMarkup([keyboard])
    update.message.reply_text('Create VM: {}.'
                              '\nPlease go to dashboard to view'
                              '\nBye Bye'.format(name_vm))


def back_page_1(bot, update):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Check agent",
                                      callback_data='check'),
                 InlineKeyboardButton("VM detail",
                                      callback_data='vm')],
                [InlineKeyboardButton("Create VM", callback_data='create')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup)
    return CHOOSING


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('nova', handle)],
    states={
    CHOOSING: [CallbackQueryHandler(choose)],
    FIRST: [CallbackQueryHandler(first)],
    SECOND: [CallbackQueryHandler(second)],
    THIRD: [CallbackQueryHandler(third)],
    FOURTH: [CallbackQueryHandler(choose_name)],
    FIFTH: [MessageHandler(Filters.text, name)]
    },
    fallbacks=[CommandHandler('nova', handle)]
)

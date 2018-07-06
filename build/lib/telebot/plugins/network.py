"""Network plugin
/network in openstack!
"""
import ipaddress
import pprint
from telebot.plugins import networkutils
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_NETWORK_NAME, CHOOSE_NETWORK_ADMIN, CHOOSE_NETWORK_SHARED, CREATE_NETWORK, CHOOSE_SUBNET_NAME, CHOOSE_IP_VER, \
 TYPING_SUBNET, CREATE_SUBNET = range(9)


def handle(bot, update):
    keyboard = [[InlineKeyboardButton('List network', callback_data="list_network"),
                 InlineKeyboardButton('Create network', callback_data="create_network")],
                [InlineKeyboardButton('Close', callback_data="close")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hi! Welcome to network function",
        reply_markup=reply_markup)

    return CHOOSING


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def choose(bot, update):
    query = update.callback_query
    query_data = query.data
    if query_data == 'list_network' or query_data == 'back_list_network':
        list_network(bot, query)
        return CHOOSING
    elif query_data.startswith('list_network_') or query_data == 'back_list_network_menu':
        list_network_menu(bot, query)
        return CHOOSING
    elif query_data == 'back_network_menu':
        menu_network(bot, query)
        return CHOOSING
    elif query_data.startswith('detail_network_'):
        detail_network(bot, query)
        return ConversationHandler.END
    elif query_data.startswith('subnet_menu_') or query_data.startswith('b_subn_menu_'):
        menu_subnet(bot, query)
        return CHOOSING
    elif query_data.startswith('list_subnet_'):
        list_subnet(bot, query)
        return CHOOSING
    elif query_data.startswith('create_subnet_'):
        print(update)
        return CHOOSE_SUBNET_NAME
        # choose_subnet_name(bot, update)

    elif query_data.startswith('subnet_'):
        list_subnet_menu(bot, query)
        return CHOOSING
    elif query_data.startswith('detail_subnet_'):
        detail_subnet(bot, query)
        return ConversationHandler.END
    elif query_data.startswith('delete_subnet_'):
        delete_subnet(bot, query)
        return ConversationHandler.END
    elif query_data.startswith('delete_network_'):
        delete_network(bot, query)
        return ConversationHandler.END
    elif query_data == 'create_network':
        bot.edit_message_text(text="Alright, a new network. Please choose a name for your network.",
                              chat_id=query.message.chat_id, message_id=query.message.message_id)
        return CHOOSE_NETWORK_ADMIN
    elif query_data == 'close':
        close(bot, query)
        return ConversationHandler.END
    else:
        pass


def list_network(bot, query):
    list_net = []
    net = networkutils.Neutron()
    for item in net.list_network():
        print('list_network' + '_' + item["id"])

        if item["name"] == '':
            name = item['id']
        else:
            name = item["name"]

        list_net.append([InlineKeyboardButton(name, callback_data='list_network' + '_' + item["id"])])
    list_net.append([InlineKeyboardButton("<< Back to network menu", callback_data='back_network_menu')])
    print(list_net)
    reply_markup = InlineKeyboardMarkup(list_net)
    bot.edit_message_text(text='List networks id:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def list_network_menu(bot, query):
    query_data = query.data
    network_id = query_data[13:]
    print('list_network_menu network_id: ' + network_id)
    options = [[InlineKeyboardButton("Detail", callback_data='detail_network' + '_' + network_id),
                InlineKeyboardButton("Delete", callback_data='delete_network' + '_' + network_id)],
               [InlineKeyboardButton("Subnet", callback_data='subnet_menu' + '_' + network_id),
                InlineKeyboardButton("<< Back", callback_data='back_list_network')]]

    reply_markup = InlineKeyboardMarkup(options)
    bot.edit_message_text(text='Options:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def menu_network(bot, query):
    keyboard = [[InlineKeyboardButton("List network", callback_data="list_network"),
                 InlineKeyboardButton("Create network", callback_data="create_network")],
                [InlineKeyboardButton("Close", callback_data="close")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(text='Network menu:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def detail_network(bot, query):
    net = networkutils.Neutron()
    query_data = query.data
    network_id = query_data[15:]
    network_detail = net.show_network(network_id)
    output = "*Detail network*" + \
             "```" + "\n" + "ID: " + network_detail["id"] + "\n" + \
             "Name: " + network_detail["name"] + "\n" +  \
             "Description: " + network_detail["description"] + "\n" + \
             "Admin state up: " + str(network_detail["admin_state_up"]) + "\n" + \
             "Status: " + network_detail["status"] + "\n" + \
             "```"
    bot.edit_message_text(text=output,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, parse_mode='Markdown')


def menu_subnet(bot, query):
    query_data = query.data
    network_id = query_data[12:]

    options = [[InlineKeyboardButton("List subnet", callback_data='list_subnet' + '_' + network_id),
                InlineKeyboardButton("Create subnet", callback_data='create_subnet' + '_' + network_id)],
               [InlineKeyboardButton("<< Back", callback_data='back_list_network_menu')]]

    reply_markup = InlineKeyboardMarkup(options)
    bot.edit_message_text(text='Options:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def list_subnet(bot, query):
    list_subnet = []
    net = networkutils.Neutron()
    query_data = query.data
    network_id = query_data[12:]
    for item in net.list_subnet(network_id):
        print('list_subnet' + ': ' + item["id"])
        if item["name"] == '':
            name = item['id']
        else:
            name = item["name"]
        list_subnet.append([InlineKeyboardButton(name, callback_data='subnet' + '_' + item["id"])])

    list_subnet.append([InlineKeyboardButton("<< Back to subnet menu", callback_data='b_subn_menu_' + network_id)])
    reply_markup = InlineKeyboardMarkup(list_subnet)
    if len(list_subnet) > 1:
        text = 'List subnets:'
    else:
        text = 'Empty!'
    bot.edit_message_text(text=text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def choose_subnet_name(bot, update, user_data):
    network_id = update.callback_query.data[14:]
    user_data['network_id'] = network_id
    print('network_id: ' + user_data['network_id'])
    update.callback_query.message.reply_text("Alright, a new subnet. Please choose a name for your subnet.")
    return CHOOSE_IP_VER


def choose_ip_version(bot, update, user_data):
    subnet_name = update.message.text
    user_data['name'] = subnet_name
    keyboard = [[InlineKeyboardButton('4', callback_data="4"),
                 InlineKeyboardButton('6', callback_data="6")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Subnet {} has IP version: '.format(subnet_name),
        reply_markup=reply_markup)
    return TYPING_SUBNET


def typing_subnet(bot, update, user_data):
    if 'ip_version' in user_data:
        print("pass")
        pass
    else:
        ip_version = update.callback_query.data
        user_data['ip_version'] = int(ip_version)
        print('user_data: ' + str(user_data))
    update.callback_query.message.reply_text('Typing network address: (eg 192.168.1.0/24)')
    return CREATE_SUBNET


def create_subnet(bot, update, user_data):
    network_addr = update.message.text
    net = networkutils.Neutron()
    if networkutils.validate_network(network_addr):
        cidr = ipaddress.ip_network(network_addr)
        if user_data["ip_version"] == cidr.version:
            cidr_list = net.list_cidr(user_data['network_id'])
            if networkutils.check_overlaps(cidr, cidr_list):
                update.message.reply_text('Overlaps with another subnet. Type again')
            else:
                user_data['cidr'] = network_addr
                user_data['enable_dhcp'] = True
                user_data['gateway_ip'] = None
                # print(user_data)
                net.create_subnet(user_data)
                update.message.reply_text('Create subnet complete')
                return ConversationHandler.END
        else:
            update.message.reply_text('Network Address and IP version are inconsistent. Type again')
    else:
        update.message.reply_text('Incorrect format for network address. Type again')
    return CREATE_SUBNET


def list_subnet_menu(bot, query):
    query_data = query.data
    subnet_id = query_data[7:]  # subnet_

    options = [[InlineKeyboardButton("Detail", callback_data='detail_subnet' + '_' + subnet_id)],
               [InlineKeyboardButton("Delete", callback_data='delete_subnet' + '_' + subnet_id)]]

    reply_markup = InlineKeyboardMarkup(options)
    bot.edit_message_text(text='Subnet options:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)


def detail_subnet(bot, query):
    net = networkutils.Neutron()
    query_data = query.data
    subnet_id = query_data[14:]
    subnet_detail = net.show_subnet(subnet_id)
    output = "*Detail subnet*" + \
             "```" + "\n" + "ID: " + subnet_detail["id"] + "\n" + \
             "Name: " + subnet_detail["name"] + "\n" +  \
             "Description: " + subnet_detail["description"] + "\n" + \
             "IP version: " + str(subnet_detail["ip_version"]) + "\n" + \
             "Cidr: " + subnet_detail["cidr"] + "\n" + \
             "Pool: " + str(subnet_detail["allocation_pools"]) + "\n" + \
             "DNS: " + str(subnet_detail["dns_nameservers"]) + "\n" + \
             "DHCP: " + str(subnet_detail["enable_dhcp"]) + "\n" + \
             "Gateway: " + str(subnet_detail["gateway_ip"]) + "\n" + \
             "```"
    bot.edit_message_text(text=output,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, parse_mode='Markdown')


def delete_subnet(bot, query):
    net = networkutils.Neutron()
    query_data = query.data
    subnet_id = query_data[14:]
    net.delete_subnet(subnet_id)
    bot.edit_message_text(text="Delete complete",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def delete_network(bot, query):
    net = networkutils.Neutron()
    query_data = query.data
    network_id = query_data[15:]
    net.delete_network(network_id)
    bot.edit_message_text(text="Delete complete",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


# Choose Admin state up Yes or No
def network_admin_choice(bot, update, user_data):
    network_name = update.message.text
    user_data['name'] = network_name
    keyboard = [[InlineKeyboardButton('Yes', callback_data="True"),
                 InlineKeyboardButton('NO', callback_data="False")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Network {}? Yes, Would you like to assign admin state up? '.format(network_name),
        reply_markup=reply_markup)
    return CHOOSE_NETWORK_SHARED


# Choose shared Yes or No
def network_shared_choice(bot, update, user_data):
    print(update)
    user_data['admin_state_up'] = update.callback_query.data
    print(user_data)
    keyboard = [[InlineKeyboardButton('Yes', callback_data="True"),
                 InlineKeyboardButton('NO', callback_data="False")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(
        'Network {}, Admin state up : {}. Shared ?'.format(user_data['name'], user_data['admin_state_up']),
        reply_markup=reply_markup)
    return CREATE_NETWORK


def create_network(bot, update, user_data):
    net = networkutils.Neutron()
    user_data['shared'] = update.callback_query.data
    print(user_data)

    # network_options = {'name': network_name, 'admin_state_up': True, 'shared': False}
    net.create_network(user_data)
    update.callback_query.message.reply_text("Create network complete")
    return ConversationHandler.END


def close(bot, query):
    bot.edit_message_text(text='Bye bye baby',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('network', handle)],

    states={
        CHOOSING: [CallbackQueryHandler(choose),
                   ],
        TYPING_NETWORK_NAME: [MessageHandler(Filters.text, create_network)],
        CHOOSE_NETWORK_ADMIN: [MessageHandler(Filters.text, network_admin_choice, pass_user_data=True)],
        CHOOSE_NETWORK_SHARED: [CallbackQueryHandler(network_shared_choice, pass_user_data=True)],
        CREATE_NETWORK: [CallbackQueryHandler(create_network, pass_user_data=True)],
        CHOOSE_SUBNET_NAME: [CallbackQueryHandler(choose_subnet_name, pass_user_data=True)],
        CHOOSE_IP_VER: [MessageHandler(Filters.text, choose_ip_version, pass_user_data=True)],
        TYPING_SUBNET: [CallbackQueryHandler(typing_subnet, pass_user_data=True),

                        ],
        CREATE_SUBNET: [MessageHandler(Filters.text, create_subnet, pass_user_data=True)],
    },

    fallbacks=[CommandHandler('close', close)]
)

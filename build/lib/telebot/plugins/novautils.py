import glanceclient.client as glance_client
import novaclient.client as nova_client
from telebot.plugins import openstackutils
from telebot.plugins import networkutils
from telegram import InlineKeyboardButton


class Nova(openstackutils.Base):

    def __init__(self, *args):
       # super().__init__(ip, username, password, project_name)
        super().__init__(*args) 
        self.nova = nova_client.Client("2.1", session=self.sess)
        self.glance = glance_client.Client('2', session=self.sess)
        self.servers = self.nova.servers.list()
        self.services = self.nova.services.list()
        self.flavors = self.nova.flavors.list()
        self.images = self.glance.images.list()

    def list_vm(self):
        dict_servers = {}
        for server in self.servers:
            name_vm = server.name
            status_vm = server.status
            dict_servers[name_vm] = status_vm
        return dict_servers

    def control(self, name_vm, action_vm):
        for server in self.servers:
            name = server.name
            if name_vm == name:
                if action_vm == 'stop':
                    server.stop()
                if action_vm == 'start':
                    server.start()
                if action_vm == 'delete':
                    server.delete()


    def service(self):
        list_info_services = []
        for service in self.services:
            list_info_service = []
            name = service.binary
            host = service.host
            state = service.state
            list_info_service.extend([name, host, state])
            list_info_services.append(list_info_service)
        return list_info_services


    def list_images(self):
        dict_images = {}
        for image in self.images:
            dict_images[image['name']] = image['id']
        return dict_images

    def list_flavors(self):
        dict_flavors = {}
        for flavor in self.flavors:
            dict_flavors[flavor.name] = flavor.id
        return dict_flavors

    def networks(self):
        dict_networks = {}
        net = networkutils.Neutron('192.168.100.114',
                                   'admin', 'locdev', 'admin')
        networks_row = net.list_network()
#        print(networks_row)
        for network in networks_row:
            dict_networks[network['name']] = network['id']
#            print(dict_networks)
        return dict_networks
        

    def keybroad_items(self, dict_items):
        keyboard_items = []
        for item in dict_items:
#            print(item)
            Name = item
            Id = dict_items[item]
            keyboard_items.append([InlineKeyboardButton(Name,
                                                    callback_data=Id)])
        return keyboard_items

    def create_vm(self, name, image, flavor, nic):
        self.nova.servers.create(name= name,
                                 image= image,
                                 flavor= flavor,
                                 nics=[{'net-id': nic}])



import pprint
import ipaddress
from neutronclient.v2_0 import client as neutronclient

from telebot.plugins import openstackutils


def str_to_bool(s):
    """Convert from specific string to bool value"""
    if s == 'True' or s == 'true':
        return True
    elif s == 'False' or s == 'false':
        return False
    else:
        raise ValueError


def validate_address(addr):
    try:
        ipaddress.ip_address(addr)
        return True
    except(IndexError, ValueError):
        return False


def validate_network(addr):
    try:
        ipaddress.ip_network(addr)
        return True
    except(IndexError, ValueError):
        return False


def validate_ip_version(num):
    if num == '4' or num == '6':
        return int(num)
    else:
        return False


def get_address_version(addr):
    address = ipaddress.ip_address(addr)
    ver = address.version
    return ver


def get_network_version(addr):
    address = ipaddress.ip_address(addr)
    ver = address.version
    return ver


def check_overlaps(cidr, cidr_list):
    """
    Check a subnet overlaps with other subnet in the network
    :return: True if overlaps
    """
    for item in cidr_list:
        if cidr.overlaps(item):
            return True
    return False


class Neutron(openstackutils.Base):
    def __init__(self, *args):
        super().__init__(*args)
        self.neutron = neutronclient.Client(session=self.sess)
        self.networks = self.neutron.list_networks()
        self.subnets = self.neutron.list_subnets()
        self.ports = self.neutron.list_ports()
        self.agents = self.neutron.list_agents()

    # unused
    def _find_network_name_by_id(self, subnet_id):
        for item in self.subnets["subnets"]:
            if item["id"] == subnet_id and item["name"] != '':
                return item["name"]
            elif item["id"] == subnet_id:
                return '(' + item["id"][:13] + ')'
        return

    # unused
    def _count_network(self, network_name):
        """How many networks are named 'network_name'"""
        count = 0
        for network in self.networks["networks"]:
            if network['name'] == network_name:
                count += 1
        return count

    # unused
    def _check_network_id_exist(self, network_id):
        for network in self.networks["networks"]:
            if network['id'] == network_id:
                return True
        else:
            return False

    def list_network(self):
        """
        List all network
        Extract a list networks with a subset of keys
        """
        network_list = []
        for item in self.networks["networks"]:
            network_keys = {'admin_state_up', 'description', 'id', 'name', 'project_id', 'shared',
                            'status', 'subnets'}
            network_dict = {key: value for key, value in item.items() if key in network_keys}
            network_list.append(network_dict)
        return network_list

    def show_network(self, network_id):
        """Show information of network by id"""
        for network in self.list_network():
            if network['id'] == network_id:
                return network 

    def create_network(self, network_options):
        """
        Create a network
        :command: /network create <network name>
                [-admin_state_up <True/False> -shared <True/False>]
        """
        # network_options = {'name': network_name, 'admin_state_up': True, 'shared': False}  # default
        self.neutron.create_network({'network': network_options})
        return

    def _delete_port_network(self, network_id):
        """Delete all interfaces attached to network"""
        for port in self.ports['ports']:
            if port['network_id'] == network_id:
                self.neutron.delete_port(port['id'])
        return

    def delete_network(self, network_id):
        """Delete network by id """
        self._delete_port_network(network_id)
        self.neutron.delete_network(network_id)
        return 

    def list_subnet(self, network_id):
        """
        List all subnet of a network
        Extract a list subnets with a subset of keys
        """
        subnet_list = []
        for item in self.subnets["subnets"]:
            if item["network_id"] == network_id:
                subnet_keys = {'allocation_pools', 'cidr', 'dns_nameservers', 'enable_dhcp', 'gateway_ip', 'id',
                               'ip_version', 'name', 'network_id', 'project_id'}
                subnet_dict = {key: value for key, value in item.items() if key in subnet_keys}
                subnet_list.append(subnet_dict)
        return subnet_list

    def list_subnet_id(self, network_id):
        """Get all subnet id in a network"""
        for network in self.networks["networks"]:
            if network["id"] == network_id:
                return network["subnets"]

    def list_cidr(self, network_id):
        """Get all subnet cidr in network"""
        cidr_list = []
        for subnet in self.list_subnet(network_id):
            cidr_list.append(ipaddress.ip_network(subnet["cidr"]))
        return cidr_list

    def show_subnet(self, subnet_id):
        """Show information of s by id"""
        for subnet in self.subnets["subnets"]:
            if subnet['id'] == subnet_id:
                return subnet

    def create_subnet(self, subnet_options):
        """Create a subnet
            type of `subnet_options` : dict
        """
        self.neutron.create_subnet({'subnet': subnet_options})
        return

    def _delete_port_subnet(self, subnet_id):
        """Delete all interfaces attached to subnet"""
        for port in self.ports['ports']:
            for item in port['fixed_ips']:
                if item['subnet_id'] == subnet_id:
                    self.neutron.delete_port(port['id'])
        return

    def delete_subnet(self, subnet_id):
        """Delete subnet by id """
        self._delete_port_subnet(subnet_id)
        self.neutron.delete_subnet(subnet_id)
        return

    def list_agent(self):
        """
        List all agent
        Extract a list agents with a subset of keys
        """
        agent_list = []
        for item in self.agents["agents"]:
            agent_keys = {'admin_state_up', 'agent_type', 'alive', 'host', 'id', 'topic'}
            agent_dict = {key: value for key, value in item.items() if key in agent_keys}
            agent_list.append(agent_dict)
        return agent_list

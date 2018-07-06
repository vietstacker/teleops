import configparser

from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutronclient
from telebot.plugins import config



class Base:
    def __init__(self, *args):
        if len(args) == 0:
            self.ip = config.IP
            self.username = config.USERNAME
            self.password = config.PASSWORD
            self.project_name = config.PROJECT_NAME
        elif len(args) == 4:
            self.ip, self.username, self.password, self.project_name = args
        else:
            raise IOError

        auth_url = 'http://{}/identity/v3'.format(self.ip)
        auth = v3.Password(auth_url=auth_url, user_domain_name='default',
                           username=self.username, password=self.password,
                           project_domain_name='default', project_name=self.project_name)
        self.sess = session.Session(auth=auth)

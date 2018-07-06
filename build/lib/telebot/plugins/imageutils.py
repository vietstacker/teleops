import glanceclient.client as glance_client
from telebot.plugins import openstackutils


class Image(openstackutils.Base):
    def __init__(self, *args):
        #super().__init__(ip, username, password, project_name)
        super().__init__(*args)
        self.glance = glance_client.Client('2', session=self.sess)
        self.images = self.glance.images.list()


    def list_images(self):
        dict_images = {}
        for image in self.images:
            dict_images[image['name']] = image['id']
        return dict_images

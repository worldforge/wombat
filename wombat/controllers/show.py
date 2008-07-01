import logging

from wombat.lib.base import *
from pylons import config

log = logging.getLogger(__name__)

class ShowController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Welcome'
        c.messages = []
        return render('/index.mako')


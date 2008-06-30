import logging

from wombat.lib.base import *
from pylons import config
import os
import os.path
import cPickle

log = logging.getLogger(__name__)

class ShowController(BaseController):

    def index(self):
        c.name = 'WOMBAT'
        c.title = 'Welcome'
        c.messages = []
        return render('/index.mako')


import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons import config
from wombat.lib.base import *
from wombat.model import Tag, File, Dir

from wombat.lib.base import BaseController

log = logging.getLogger(__name__)

class TagController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Tag view'
        c.messages = []
        c.session = Session()

        tags = c.session.query(Tag).all()
        used_tags = []
        for tag in tags:
            count = len(tag.assets) + len(tag.collections)
            if count > 0:
                used_tags.append(tag)

        c.tags = used_tags

        return render('/derived/tag/index.html')


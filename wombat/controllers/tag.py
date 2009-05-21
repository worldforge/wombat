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
        max_count = 0
        for tag in tags:
            count = len(tag.assets) + len(tag.collections)
            if count > 0:
                if count > max_count:
                    max_count = count
                used_tags.append((tag, count))

        ranked_tags = []
        for tag, count in used_tags:
            percentage = float(count) / float(max_count)
            if percentage < 0.5:
                ranked_tags.append((tag, 'normal', count))
            elif percentage < 0.75:
                ranked_tags.append((tag, 'popular', count))
            elif percentage < 1:
                ranked_tags.append((tag, 'very-popular', count))
            else:
                ranked_tags.append((tag, 'top', count))

        ranked_tags.sort()
        c.tags = ranked_tags

        return render('/derived/tag/index.html')


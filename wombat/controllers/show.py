import logging
import os.path
import cPickle
import time

from wombat.lib.base import *
from pylons import config

log = logging.getLogger(__name__)

class ShowController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Welcome'
        c.messages = []

        if not os.path.exists(config.get('app_conf').get('rootdir_cache')):
            c.messages.append("Failed to locate cached data.")
            return render('/derived/show/please_scan.html')

        f = open(config.get('app_conf').get('rootdir_cache'), 'r')
        try:
            c.root_dir = cPickle.load(f)
        finally:
            f.close()

        return render('/derived/show/index.html')

    def search(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Search results'
        c.messages = []

        if not os.path.exists(config.get('app_conf').get('rootdir_cache')):
            c.messages.append("Failed to locate cached data.")
            return render('/derived/show/please_scan.html')

        f = open(config.get('app_conf').get('rootdir_cache'), 'r')
        try:
            c.root_dir = cPickle.load(f)
        finally:
            f.close()

        try:
            c.needle = request.params['match']
        except KeyError:
            c.needle = ""

        try:
            c.match_author = request.params['author']
        except KeyError:
            c.match_author = ""


        try:
            c.match_ext = request.params['extension']
        except KeyError:
            c.match_ext = ""

        try:
            c.match_date_in = request.params['date_in']
        except KeyError:
            c.match_date_in = ""

        try:
            c.match_date_out = request.params['date_out']
        except KeyError:
            c.match_date_out = ""

        date_in = h.dateStrToEpoch(c.match_date_in)
        date_out = h.dateStrToEpoch(c.match_date_out)

        c.results = h.search(c.root_dir, c.needle,
                c.match_author, c.match_ext, date_in, date_out )

        return render('/derived/show/searchresults.html')


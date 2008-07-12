import logging
import os.path
import cPickle

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
            return render('/please_scan.mako')

        f = open(config.get('app_conf').get('rootdir_cache'), 'r')
        try:
            c.root_dir = cPickle.load(f)
        finally:
            f.close()

        return render('/index.mako')

    def search(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Search results'
        c.messages = []

        if not os.path.exists(config.get('app_conf').get('rootdir_cache')):
            c.messages.append("Failed to locate cached data.")
            return render('/please_scan.mako')

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

        # We need some helper to handle date range parameter to secs since epoch
        # conversion.

        c.found_dirs, c.found_files = c.root_dir.search(c.needle,
                c.match_author, c.match_ext)

        return render('/searchresults.mako')


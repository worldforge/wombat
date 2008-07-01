import logging

from wombat.lib.base import *
from pylons import config
import os
import os.path
import cPickle

log = logging.getLogger(__name__)

class DirController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Directory view'
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
            req_path = request.params['path']
        except KeyError:
            req_path = ""
        c.req_path = req_path
        try:
            c.dir = c.root_dir.getDir(req_path)
        except KeyError:
            c.dir = c.root_dir
        return render('/dir.mako')


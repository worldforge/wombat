import logging

from wombat.lib.base import *
from pylons import config
import os.path
import cPickle

log = logging.getLogger(__name__)

class FileController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'File view'
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
            req_path = request.params['path']
        except KeyError:
            req_path = ""
        c.req_path = req_path
        try:
            c.obj = c.root_dir.getFile(req_path)
        except KeyError:
            c.messages.append("Failed to locate file '%s'." % req_path)
            c.obj = c.root_dir
            return render('/derived/dir/dir.html')
        return render('/derived/file/file.html')

    def panel(self):
        c.name = config['app_conf']['site_name']
        c.title = 'File view'
        if not os.path.exists(config.get('app_conf').get('rootdir_cache')):
            c.messages.append("Failed to locate cached data.")
            return ""

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
            c.obj = c.root_dir.getFile(req_path)
        except KeyError:
            c.messages.append("Failed to locate file '%s'." % req_path)
            c.obj = c.root_dir
            return ""

        panel = render('/derived/file/details.html')
        panel += render('/derived/file/pagination.html')
        return panel


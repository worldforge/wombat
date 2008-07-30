import logging

from wombat.lib.base import *
import os
import os.path
import cPickle

log = logging.getLogger(__name__)

class ScanController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan mode'
        c.messages = []
        return render('/derived/scan/scan.html')

    def scan(self):
        from wombat.model.rootdir import RootDir

        if not h.canScan():
            redirect_to(action="index")

        dir = RootDir(config['app_conf']['media_dir'])
        dir.scan()
        if not os.path.exists(config['cache.dir']):
            os.mkdir(config['cache.dir'])
        f = open(config['app_conf']['rootdir_cache'], 'w')
        try:
            cPickle.dump(dir, f, -1)
        finally:
            f.close()

        h.createScanLock()

        redirect_to(action="result")

    def result(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan complete'
        c.messages = []
        return render('/derived/scan/scan_complete.html')


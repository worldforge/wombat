import logging

from wombat.lib.base import *
import os
import os.path
import cPickle

log = logging.getLogger(__name__)

class ScanController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'

    def scan(self):
        from wombat.model.rootdir import RootDir

        dir = RootDir(config['app_conf']['media_dir'])
        dir.scan()
        if not os.path.exists(config.get('cache.dir')):
            os.mkdir(config.get('cache.dir'))
        f = open(config.get('app_conf').get('rootdir_cache'), 'w')
        try:
            cPickle.dump(dir, f, -1)
        finally:
            f.close()

        c.name = 'WOMBAT'
        c.title = 'Scanning the repository'
        return "SCANNING"


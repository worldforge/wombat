import logging

from wombat.lib.base import *
from wombat.lib.backend import scan, update

log = logging.getLogger(__name__)

class ScanController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan mode'
        c.messages = []
        c.session = Session()
        return render('/derived/scan/scan.html')

    def scan(self):
        if not h.canScan():
            redirect_to(action="index")

        c.session = Session()
        scan(c.session)
        h.createScanLock()

        redirect_to(action="result")

    def result(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan complete'
        c.messages = []
        c.session = Session()
        return render('/derived/scan/scan_complete.html')

    def update(self):
        # if we never scanned before, do so now.
        if h.canScan():
            redirect_to(action="scan")

        c.session = Session()
        update(c.session)
        redirect_to(action="result")


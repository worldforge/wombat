import logging

from wombat.lib.base import *
from wombat.lib.backend import scan

log = logging.getLogger(__name__)

class ScanController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan mode'
        c.messages = []
        return render('/derived/scan/scan.html')

    def scan(self):
        if not h.canScan():
            redirect_to(action="index")

        session = Session()

        scan(session)

        h.createScanLock()

        redirect_to(action="result")

    def result(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan complete'
        c.messages = []
        return render('/derived/scan/scan_complete.html')


import logging

from wombat.lib.base import *
from wombat.lib.backend import scan, update
from wombat.lib.roles import require_roles, require_login

log = logging.getLogger(__name__)

class ScanController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan mode'
        c.messages = []
        c.session = Session()
        return render('/derived/scan/scan.html')

    @require_login
    def scan(self):
        c.session = Session()
        if not h.canScan(c.session):
            redirect_to(action="index")

        scan(c.session)

        redirect_to(action="result")

    def result(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Scan complete'
        c.messages = []
        c.session = Session()
        return render('/derived/scan/scan_complete.html')

    @require_login
    def update(self):
        c.session = Session()
        # if we never scanned before, do so now.
        if h.canScan(c.session):
            redirect_to(action="scan")

        update(c.session)
        redirect_to(action="result")


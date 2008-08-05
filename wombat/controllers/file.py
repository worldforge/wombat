import logging

from wombat.lib.base import *
from pylons import config
from wombat.model import File

log = logging.getLogger(__name__)

class FileController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'File view'
        c.messages = []

        session = Session()

        try:
            req_path = request.params['path']
        except KeyError:
            req_path = ""

        c.file = session.query(File).filter_by(path=req_path).first()
        if c.file is None:
            abort(404)

        return render('/derived/file/file.html')

    def panel(self):
        session = Session()

        try:
            req_path = request.params['path']
        except KeyError:
            req_path = ""

        c.file = session.query(File).filter_by(path=req_path).first()
        if c.file is None:
            abort(404)

        panel = render('/derived/file/details.html')
        panel += render('/derived/file/pagination.html')
        return panel

    def unassigned(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Unassigned files'
        c.messages = []

        session = Session()
        c.unassigned = session.query(File).filter_by(used_by=None).all()
        return render('/derived/file/unassigned.html')


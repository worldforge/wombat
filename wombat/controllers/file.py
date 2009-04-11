import logging

from wombat.lib.base import *
from pylons import config
from wombat.model import File, Asset, Tag

log = logging.getLogger(__name__)

class FileController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'File view'
        c.messages = []

        c.session = Session()

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u""

        c.file = c.session.query(File).filter_by(path=req_path).first()
        if c.file is None:
            abort(404)

        c.dir = c.file.directory
        if c.dir is None:
            c.dir = ""

        return render('/derived/file/file.html')

    def panel(self):
        c.session = Session()

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u""

        c.file = c.session.query(File).filter_by(path=req_path).first()
        if c.file is None:
            abort(404)

        panel = render('/derived/file/details.html')
        panel += render('/derived/file/pagination.html')
        return panel

    def unassigned(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Unassigned files'
        c.messages = []

        c.session = Session()
        c.unassigned = c.session.query(File).filter_by(used_by=None).all()
        return render('/derived/file/unassigned.html')

    def tagged(self, id=None):
        if id is None:
            abort(404)

        c.name = config['app_conf']['site_name']
        c.title = "Files tagged by '%s'" % id
        c.messages = []

        c.session = Session()
        tags = id.split(u'+')
        aq = c.session.query(Asset)
        tag_ids = []
        for tag_name in tags:
            tag = c.session.query(Tag).filter(Tag.name == tag_name).first()
            aq = aq.filter(Asset.tags.contains(tag))
        assets = aq.all()
        if assets is None:
            abort(404)
        c.id = id
        tagged = []
        for asset in assets:
            tagged.extend(asset.files)
        c.tagged = tagged
        return render('/derived/file/tagged.html')


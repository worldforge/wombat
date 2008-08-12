import logging

from wombat.lib.base import *
from pylons import config
import os.path
from wombat.model import Dir, File
from sqlalchemy.sql import select
log = logging.getLogger(__name__)

class DirController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Directory view'
        c.messages = []

        c.session = Session()

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u"."
        c.req_path = req_path

        c.dir = c.session.query(Dir).get(req_path)
        if c.dir is None:
            abort(404)

        groups = c.session.execute(select([File.type], distinct=True)).fetchall()

        c.groups = {}
        for group in groups:
            c.groups[group[0]] = c.session.query(File).filter_by(in_dir=c.dir.path).filter_by(type=group[0]).all()

        return render('/derived/dir/dir.html')


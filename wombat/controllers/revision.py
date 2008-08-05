import logging

from wombat.lib.base import *
from wombat.model import Revision

log = logging.getLogger(__name__)

class RevisionController(BaseController):

    def show(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Revision view'
        c.messages = []

        if id is None:
            abort(404)
        c.session = Session()
        revision = c.session.query(Revision).filter_by(id=int(id)).first()
        if revision is None:
            abort(404)

        c.revision = revision
        c.session = session

        return render('/derived/revision/show.html')

    def details(self, id):
        if id is None:
            abort(404)
        c.session = Session()
        revision = c.session.query(Revision).filter_by(id=int(id)).first()
        if revision is None:
            abort(404)

        c.revision = revision

        return render('/derived/revision/details.html')



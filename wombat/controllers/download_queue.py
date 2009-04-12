import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons import config

from wombat.lib.base import BaseController, Session, render
from wombat.lib.roles import require_roles, require_login
from wombat.model import User, DownloadQueue, File

log = logging.getLogger(__name__)

class DownloadQueueController(BaseController):

    @require_login
    def show(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Download Queue view'
        c.messages = []

        if not 'user' in session:
            abort(404)
        c.session = Session()
        user = c.session.query(User).get(session['user'])
        if user is None:
            abort(404)

        c.dl_queue = user.download_queue

        return render('/derived/download_queue/show.html')

    @require_login
    def add(self):
        if not 'user' in session:
            abort(404)

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u""

        c.session = Session()
        user = c.session.query(User).get(session['user'])
        if user is None:
            abort(404)

        file = c.session.query(File).get(req_path)
        if file is None:
            abort(404)

        queue = user.download_queue
        if not queue:
            queue = DownloadQueue()
            queue.user = user
            c.session.save(queue)

        if not file in user.download_queue.files:
            user.download_queue.files.append(file)

        c.session.commit()
        return "Added"

    @require_login
    def remove(self):
        if not 'user' in session:
            abort(404)

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u""

        c.session = Session()
        user = c.session.query(User).get(session['user'])
        if user is None:
            abort(404)

        file = c.session.query(File).get(req_path)
        if file is None:
            abort(404)

        if not user.download_queue:
            return "Removed"

        if file in user.download_queue:
            user.download_queue.files.remove(file)

        return "Removed"

    @require_login
    def download(self):
        if not 'user' in session:
            abort(404)

        c.session = Session()
        user = c.session.query(User).get(session['user'])
        if user is None:
            abort(404)

        name = user.user_data.nick and user.user_data.nick or user.email.replace(u'@', u'_')
        c.download_name = "%s_queued_download.zip" % name

        #TODO: Implement creating the download archive

        return c.download_name


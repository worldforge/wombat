import logging

from wombat.lib.base import *
from wombat.lib.backend import add, commit
from pylons.decorators.secure import authenticate_form
from pylons import config
import os.path
import re
from wombat.lib.roles import require_login
from wombat.model import Dir, File
from sqlalchemy.sql import select
log = logging.getLogger(__name__)
from routes import url_for

class DirController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Directory view'
        c.messages = []

        c.session = Session()
        c.upload = True

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

    def dir_li(self):
        c.session = Session()

        try:
            req_path = unicode(request.params['path'])
        except KeyError:
            req_path = u""

        c.dir = c.session.query(Dir).get(req_path)
        if c.file is None:
            abort(404)
        return render('/derived/dir/dir_li.html')

    @require_login
    def create(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Create directory'
        c.messages = []

        c.session = Session()

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        path = str(request.params.get('path', None))
        if path is None:
            abort(404)

        c.path = path

        return render('/derived/dir/create.html')

    @authenticate_form
    @require_login
    def createdir(self):
        c.session = Session()
        media_dir = config['app_conf']['media_dir']

        path = unicode(request.params.get('path', None))
        if path is None:
            abort(404)

        check_dir = c.session.query(Dir).get(path)
        if check_dir is None:
            abort(404)

        create_dir = request.params.get('createdir', None)
        if create_dir is None:
            return redirect_to(url_for(controller="dir") + "?path=" + str(create_dir))

        #Can start with a single .  max len = 32
        #No space because I'm experimenting problems with the add function
        p = re.compile("^[A-Za-z0-9_.][A-Za-z0-9_]{0,31}$")
        if not p.match(create_dir):
            session['messages'] = ['Invalid subdirectory name']
            session.save()
            return redirect_to(url_for(controller="dir", action="create") + "?path=" + str(check_dir.path))

        if not check_dir.path == ".":
            create_dir =  os.path.join(check_dir.path, create_dir)

        if c.session.query(Dir).get(create_dir) is None:
            message = "Dir : \'%s\' created" % create_dir
            os.mkdir( os.path.join(media_dir, create_dir))
            add(create_dir, Session())
            commit([create_dir], message, session['user'], Session())
            #Error handeling
        else:
            session['messages'] = ['Subdirectory already exist']
            session.save()
            return redirect_to(str('/dir/create?path=' + check_dir.path))

        return redirect_to(url_for(controller="dir") + "?path=" + str(create_dir))


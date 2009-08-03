# Copyright (C) 2009 by Cedric Marechal
#
# WOMBAT is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA

import logging

from wombat.lib.base import *
from wombat.lib.backend import add, commit
from pylons import config
from wombat.lib.roles import require_roles, require_login
from pylons.decorators.secure import authenticate_form
from wombat.model import Upload
from wombat.lib.fetch import fetch_file, get_path

import os
import shutil

from routes import url_for

log = logging.getLogger(__name__)

class ModerationController(BaseController):

    @require_roles(['lead'])
    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Moderate'
        c.messages = []
        c.session = Session()
        s = Session()

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        #Only one project now
        c.modfilelist = s.query(Upload).filter(Upload.status == None).all()
        c.comfilelist = s.query(Upload).filter(Upload.status == u"Moderated").all()

        return render('/derived/moderation/index.html')

    @require_roles(['lead'])
    def view(self):
        c.name = config['app_conf']['site_name']
        c.title = 'View'
        c.messages = []
        c.session = Session()

        file = request.params.get('file', None)
        if file is None:
            return redirect_to(url_for(controller="moderation"))

        #Get the image/FILE
        file = fetch_file(file)

        if 'error' in file:
            session['messages'] = ["Invalid file"]
            session.save()
            return redirect_to(url_for(controller="moderation"))

        if 'scr' in file:
            c.scr = file['scr']
        elif 'href' in file:
            c.href = file['href']
        c.filename = file['filename']
        c.new_name = file['new_name']
        c.description = file['description']
        c.destination = file['destination']
        c.author = file['author']
        c.status = file['status']


        return render('/derived/moderation/view.html')

    @require_roles(['lead'])
    def servefile(self, new_name, name):

        path = get_path("moderation")
        extList = ["jpeg", "jpg", "png", "gif"]
        s = Session()

        db_file = s.query(Upload).get(new_name)
        if db_file is None:
            abort(404)
        file_type = db_file.file_type.strip('.')
        if file_type in extList:
            response.content_type = "image/" + file_type
        else:
            response.content_type = "application/octet-stream"

        path = os.path.join(path, new_name)
        f = open(path, 'r')
        return f

    @require_roles(['lead'])
    def rejected(self):
        s = Session()

        new_name = request.params.get('name', None)
        if new_name is None:
            abort(404)

        db_file = s.query(Upload).get(new_name)

        if db_file is None:
            session['messages'] = ["Invalid file"]
            session.save()
            return redirect_to(url_for(controller="moderation"))

        path = os.path.join(get_path("moderation"), db_file.new_name)
        #TODO error handeling
        if os.path.exists(path):
            os.remove(path)

        s.delete(db_file)
        s.commit()

        session['messages'] = ["File rejected"]
        session.save()
        return redirect_to(url_for(controller="moderation"))

    @require_roles(['lead'])
    def accepted(self):
        s = Session()

        new_name = request.params.get('name', None)
        if new_name is None:
            abort(404)

        db_file = s.query(Upload).get(new_name)

        if db_file is None:
            session['messages'] = ["Invalid file"]
            session.save()
            return redirect_to(url_for(controller="moderation"))

        db_file.status = u"Moderated"
        s.commit()

        return redirect_to(url_for(controller="moderation"))

    @require_roles(['lead'])
    def remove(self):
        s = Session()

        new_name = request.params.get('name', None)
        if new_name is None:
            abort(404)

        db_file = s.query(Upload).get(new_name)

        if db_file is None:
            session['messages'] = ["Invalid file"]
            session.save()
            return redirect_to(url_for(controller="moderation"))

        db_file.status = None
        s.commit()

        return redirect_to(url_for(controller="moderation"))

    @authenticate_form
    @require_roles(['lead'])
    def commit(self):
        s = Session()
        session['messages'] = []
        paths = []

        message = request.params.get("message", "Web commit")
        db_files = s.query(Upload).filter(Upload.status == u"Moderated").all()
        for db_file in db_files:

            destination = get_path(None, db_file.destination)
            if destination == "Invalid path":
                session['messages'] += ["Invalid destination for the file %s" % db_file.name]
                session.save()
                return redirect_to(url_for(controller="moderation"))

            currentpath = os.path.join(get_path("moderation"), db_file.new_name)
            #os.sep is to fix a bug
            shutil.move(currentpath, destination+os.sep)

            oldpath = os.path.join(destination, db_file.new_name)
            path = os.path.join(destination, db_file.name)
            os.rename(oldpath, path)

            #TODO error handling
            path = os.path.join(db_file.destination, db_file.name)
            add(path, Session())
            paths += [path]
            session['messages'] += ["%s is commit" % db_file.name]
            session.save()
            s.delete(db_file)
            s.commit()

        commit(paths, message, session['user'], Session())

        return redirect_to(url_for(controller="moderation"))


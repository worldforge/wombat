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
from pylons import config
from wombat.lib.roles import require_login
from pylons.decorators.secure import authenticate_form
from wombat.model import Upload, Dir, UserData
import re

import os
import shutil
from routes import url_for
import random

log = logging.getLogger(__name__)


class UploadController(BaseController):

    @require_login
    def index(self):

        c.name = config['app_conf']['site_name']
        c.title = 'Upload'
        c.messages = []
        c.session = Session()

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        if not os.path.exists(config['app_conf']['upload_dir']):
            os.makedirs(config['app_conf']['upload_dir'])

        form_dir = request.params.get('path', None)
        if form_dir is None:
            abort(404)
        destination = c.session.query(Dir).get(form_dir)
        if destination is None:
            abort(404)
        else:
            c.destination = destination.path

        return  render('/derived/upload/index.html')

    @authenticate_form
    @require_login
    def upload(self):

        c.session = Session()
        session['messages'] = []
        author = c.session.query(UserData).get(session['user']).name
        VALID_CHARS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        uri_dir = request.params.get('path', None)
        if uri_dir is None:
            abort(404)
        destination = c.session.query(Dir).get(uri_dir)
        if destination is None:
            abort(404)
        else:
            destination = destination.path

        myfiles = request.POST.getall('myfile')

        for myfile in myfiles:
            if myfile == "":
               return redirect_to(url_for(controller="upload") + '?path=' + str(uri_dir))

            original_name = myfile.filename
            myfile.filename = u"".join(random.sample(VALID_CHARS, 16))
            permanent_file = open(os.path.join(config['app_conf']['upload_dir'], myfile.filename), 'w')

            shutil.copyfileobj(myfile.file, permanent_file)

            #add it to the Upload database
            p = re.compile("^[A-Za-z0-9_.][A-Za-z0-9_.-]{0,99}$")
            if not p.match(original_name):
                session['messages'] += ['ERROR invalid filename : %s' % (original_name)]
                session.save()
            else:
                filename = original_name
                ext = os.path.splitext(filename)[1].lower()
                db_file = Upload(name = filename,
                                file_type = ext,
                                destination = destination,
                                description = request.POST.get('description', ''),
                                new_name = myfile.filename,
                                author = author)

                Session.add(db_file)
                Session.commit()

                myfile.file.close()
                permanent_file.close()

                #Security?
                session['messages'] += ['Successfully uploaded: %s' % (original_name)]
                session.save()

        return redirect_to(url_for(controller="upload") + '?path=' + str(uri_dir))

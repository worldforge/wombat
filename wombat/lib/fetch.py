# Copyright (C) 2008 by Kai Blin
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

import os
from pylons import config
from wombat.lib.base import *

from wombat.model import Upload, Dir
from routes import url_for

def get_path(project, destination = None):

    if project == "moderation":
        path = config['app_conf']['upload_dir']
    elif destination is not None:
        check_dir = Session.query(Dir).get(destination)
        if check_dir is None:
            return "Invalid path"
        if check_dir.path == ".":
            path = config['app_conf']['media_dir']
        else:
            path = os.path.join(config['app_conf']['media_dir'], check_dir.path)

    return path


def fetch_file(name):

    s = Session()
    result = {}
    extList = ["jpeg", "jpg", "png", "gif"]

    db_file = s.query(Upload).filter(Upload.new_name==name).first()
    if db_file is None:
        result['error'] = "Invalid file"

    result['new_name'] = db_file.new_name
    result['filename'] = db_file.name
    result['description'] = db_file.description
    result['destination'] = db_file.destination
    result['author'] = db_file.author
    result['status'] = db_file.status

    file_type = db_file.file_type.strip('.')
    if file_type in extList:
        result['scr'] = "/uploads/" + db_file.new_name + "/" + db_file.name
    else:
        result['href'] = "/uploads/" + db_file.new_name + "/" +db_file.name


    return result

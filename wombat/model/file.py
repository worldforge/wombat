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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import types, schema
from os.path import splitext
from wombat.lib.helpers import getType

def init_files_table(metadata):
    return Table('files', metadata,
        Column('path', types.Unicode(255), primary_key=True),
        Column('name', types.Unicode(255)),
        Column('size', types.Integer),
        Column('root', types.Unicode(255)),
        Column('ext', types.Unicode(20)),
        Column('type', types.Unicode(20), default=u"other"),
        Column('as_thumbnail', types.Boolean, default=False),
        Column('in_dir', types.Unicode(255), schema.ForeignKey('dirs.path')),
        Column('rev_id', types.Integer, schema.ForeignKey('revisions.id')),
        Column('used_by', types.Integer, schema.ForeignKey('assets.id'))
    )

class File(object):
    def __init__(self, path, name, size, root):
        self.path = path
        self.name = name
        self.size = size
        self.root = root
        dummy, self.ext = splitext(name)
        self.ext = self.ext.lower()
        self.type = unicode(getType(name))



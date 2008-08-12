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

def init_dirs_table(metadata):
    return Table('dirs', metadata,
        Column('path', types.Unicode(255), primary_key=True),
        Column('name', types.Unicode(255)),
        Column('root', types.Unicode(255)),
        Column('rev_id', types.Integer, schema.ForeignKey('revisions.id')),
        Column('in_dir', types.Unicode(255), schema.ForeignKey('dirs.path'))
    )

class Dir(object):
    def __init__(self, path, name, root):
        self.path = path
        self.name = name
        self.root = root


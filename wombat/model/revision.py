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

from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import types, schema

def init_rev_table(metadata):
    return Table('revisions', metadata,
        Column('id', types.Integer, primary_key=True),
        Column('name', types.Unicode(255), default=''),
        Column('log', types.Text(), default=u'No log message'),
        Column('author', types.Unicode(255), default=u'Unknown Author'),
        Column('date', types.DateTime())
    )

class Revision(object):
    def __init__(self, id, name, log, author, date):
        self.id = id
        self.name = name
        self.log = log
        self.author = author
        self.date = date



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

def init_assets_table(metadata):
    return Table('assets', metadata,
        Column('id', types.Integer, primary_key=True),
        Column('name', types.Unicode(255), default=u'Unnamed Asset'),
        Column('keywords', types.Unicode(255)),
        Column('used_by', types.Integer, schema.ForeignKey('collections.id'))
    )

class Asset(object):
    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords


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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import types, schema


def init_uploads_table(metadata):
    return Table('Upload', metadata,
        Column('name',  types.Unicode(255)),
        Column('file_type',  types.Unicode(255)),
        Column('destination',  types.Unicode(255)),
        Column('description',  types.Unicode(255)),
        Column('new_name',  types.Unicode(255), primary_key=True),
        Column('author' , types.Unicode(255)),
        Column('status' , types.Unicode(255)))

class Upload(object):
    def __init__(self, name, file_type, destination, description, new_name, author, status=None):
        self.name = name
        self.file_type = file_type
        self.destination = destination
        self.description = description
        self.new_name = new_name
        self.author = author
        self.status = status



# Copyright (C) 2009 by Kai Blin
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

def init_download_queue_table(metadata):
    return Table('download_queues', metadata,
        Column('id', types.Integer, primary_key=True),
        Column('user_id', types.Integer, schema.ForeignKey('users.id'))
    )

class DownloadQueue(object):
    def __init__(self):
        pass

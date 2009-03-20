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

from sqlalchemy import Table, Column, types
from datetime import datetime

def init_email_confirm_table(metadata):
    return Table('email_confirm', metadata,
        Column('id', types.Integer, primary_key=True),
        Column('token', types.Unicode(255)),
        Column('email', types.Unicode(255)),
        Column('date', types.DateTime),
    )

class EmailConfirm(object):
    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.date = datetime.now()


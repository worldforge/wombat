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

from threading import Timer
import time
import datetime

def cleanup_email_confirm():
    """Clean up the old entries from the EmailConfirm table"""
    from wombat.model import meta, EmailConfirm, User
    s = meta.Session()
    delta = datetime.timedelta(days=2)
    now = datetime.datetime.now()
    to_delete = s.query(EmailConfirm).filter(EmailConfirm.date < now - delta).all()
    for item in to_delete:
        user = s.query(User).filter(User.email == item.email).first()
        s.delete(item)
        if user and not user.active:
            s.delete(user.user_data)
            s.delete(user)
    s.commit()
    meta.Session.remove()

def cleanup_reset_data():
    from wombat.model import meta, ResetData
    s = meta.Session()
    delta = datetime.timedelta(days=2)
    now = datetime.datetime.now()
    to_delete = s.query(ResetData).filter(ResetData.date < now - delta).all()
    for item in to_delete:
        s.delete(item)
    s.commit()
    meta.Session.remove()

def cleanup_dbs(globals):
    globals.scan_lock.acquire()
    cleanup_email_confirm()
    cleanup_reset_data()
    globals.scan_lock.release()

    globals.last_cleanup = time.ctime()

    globals.cleanup_timer = Timer(3600.0, cleanup_dbs, [globals])
    globals.cleanup_timer.start()




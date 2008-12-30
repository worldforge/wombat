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

def update_media(globals):
    from wombat.lib.backend import fetch, update
    from wombat.model import Session
    from wombat.lib.helpers import canScan

    fetch(globals)

    globals.update_status = "Updating database"

    s = Session()
    if not canScan(s):
        globals.scan_lock.acquire()
        update(s)
        globals.scan_lock.release()
        globals.update_status = "Update complete"
    else:
        globals.update_status = "Update denied"

    globals.update_timer = Timer(300.0, update_media, [globals])
    globals.update_timer.start()

    Session.remove()


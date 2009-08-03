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

from decorator import decorator
from wombat.lib.base import *
from wombat.model import User

def require_roles(roles):
    @decorator
    def check_roles(fn, *args, **kwargs):
        # if a role is required, the user needs to be logged in.
        if not 'user' in session:
            # Remember original requested path
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(h.url_for(controller='auth', action='login'))

        s = Session()

        user = s.query(User).get(session['user'])
        if user is None:
            #something's wrong here.
            abort(403)

        for role in roles:
            # If the user has the role required, go on with the original
            # function
            for i in range(len(user.roles)):
                if role == user.roles[i].name:
                    s.close()
                    return fn(*args, **kwargs)

            # special case where we want to make sure the "id" arg matches the
            # user's id
            if role == 'owner':
                if len(args) < 2:
                    continue

                try:
                    id = int(args[1])
                except ValueError:
                    continue

                if id == user.id:
                    s.close()
                    return fn(*args, **kwargs)

        # checked all the roles, no match.
        abort(403)

    return check_roles

@decorator
def require_login(fn, *args, **kwargs):
    if not 'user' in session:
        # Remember original requested path
        session['path_before_login'] = request.path_info
        session.save()
        return redirect_to(h.url_for(controller='auth', action='login'))

    return fn(*args, **kwargs)

def check_role(role):
    s = Session()

    user = s.query(User).get(session['user'])
    for i in range(len(user.roles)):
        if role == user.roles[i].name:
            return True
    return False


"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

import wombat.lib.helpers as h
import wombat.model as model

from wombat.model import Session

class BaseController(WSGIController):
    needs_auth = []

    def __before__(self, action):
        # Check if authentication is reqired
        if action in self.needs_auth and 'user' not in session:
            # Remember original requested path
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(h.url_for(controller='login'))


    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']

import logging

from wombat.lib.base import *

log = logging.getLogger(__name__)

class FileController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Implement me!'

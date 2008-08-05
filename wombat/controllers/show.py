import logging
import os.path
import cPickle
import time

from wombat.lib.base import *
from pylons import config
from wombat.model import Revision, File

log = logging.getLogger(__name__)

class ShowController(BaseController):

    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Welcome'
        c.messages = []

        session = Session()

        file_q = session.query(File)

        first_file = file_q.first()

        if first_file is None:
            return render('/derived/show/please_scan.html')

        c.repo_url = first_file.root
        c.total_size = file_q.sum(File.size)
        c.avg_size = file_q.avg(File.size)

        c.revision = session.query(Revision).max(Revision.id)

        return render('/derived/show/index.html')

    def search(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Search results'
        c.messages = []

        try:
            c.needle = request.params['match']
        except KeyError:
            c.needle = ""

        try:
            c.match_author = request.params['author']
        except KeyError:
            c.match_author = ""

        try:
            c.match_ext = request.params['extension']
        except KeyError:
            c.match_ext = ""

        try:
            c.match_date_in = request.params['date_in']
        except KeyError:
            c.match_date_in = ""

        try:
            c.match_date_out = request.params['date_out']
        except KeyError:
            c.match_date_out = ""

        session = Session()
        file_q = session.query(File)

        if c.needle != "":
            from sqlalchemy import or_
            file_q = file_q.filter(or_(File.name.like("%%%s%%" % c.needle),
                File.path.like("%%%s%%" % c.needle)))

        if c.match_author != "":
            file_q = file_q.filter(Revision.author == c.match_author)

        if c.match_date_in != "":
            file_q = file_q.filter(Revision.date > c.match_date_in)

        if c.match_date_out != "":
            file_q = file_q.filter(Revision.date < c.match_date_out)

        c.found_files = file_q.all()

        return render('/derived/show/searchresults.html')


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

        c.session = Session()

        file_q = c.session.query(File)

        first_file = file_q.first()

        if first_file is None:
            return render('/derived/show/please_scan.html')

        c.repo_url = first_file.root
        c.total_size = file_q.sum(File.size)
        c.avg_size = file_q.avg(File.size)

        # This is not pretty, but I didn't find any better way to do this from
        # the sqlalchemy.orm.query
        ext_file, count = file_q.add_column("ext_count").from_statement(\
            "SELECT files.path AS files_path, files.name AS files_name,\
            files.size AS files_size, files.root AS files_root, files.ext AS\
            files_ext, files.as_thumbnail AS files_as_thumbnail, files.rev_id\
            AS files_rev_id, files.used_by AS files_used_by, count(files.ext)\
            as ext_count FROM files GROUP BY files.ext ORDER BY\
            count(files.ext) DESC").first()

        c.ext_string = ext_file.ext
        c.ext_count = count

        c.revision = c.session.query(Revision).max(Revision.id)

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

        c.session = Session()
        file_q = c.session.query(File)

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


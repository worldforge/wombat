import logging
import os.path
import cPickle
import time

from wombat.lib.base import *
from pylons import config
from wombat.model import Revision, File, Dir, Asset, Collection

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
        c.file_count = file_q.count()
        c.avg_size = file_q.avg(File.size)

        from sqlalchemy.sql import select, func
        res = c.session.execute(select([File.ext,
            func.count(File.ext)]).group_by(File.ext).order_by(func.count(File.ext).desc())).fetchone()

        c.ext_string = res[0]
        c.ext_count = res[1]

        c.revision = c.session.query(Revision).max(Revision.id)

        c.asset_count = c.session.query(Asset).count()
        c.collection_count = c.session.query(Collection).count()

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
        dir_q = c.session.query(Dir)

        if c.needle != "":
            from sqlalchemy import or_
            file_q = file_q.filter(or_(File.name.like("%%%s%%" % c.needle),
                File.path.like("%%%s%%" % c.needle)))
            dir_q = dir_q.filter(or_(Dir.name.like("%%%s%%" % c.needle),
                Dir.path.like("%%%s%%" % c.needle)))

        if c.match_author != "":
            file_q = file_q.filter(Revision.author == c.match_author)
            dir_q = dir_q.filter(Revision.author == c.match_author)

        if c.match_ext != "":
            file_q = file_q.filter(File.ext == c.match_ext)

        if c.match_date_in != "":
            file_q = file_q.filter(Revision.date > c.match_date_in)
            dir_q = dir_q.filter(Revision.date > c.match_date_in)

        if c.match_date_out != "":
            file_q = file_q.filter(Revision.date < c.match_date_out)
            dir_q = dir_q.filter(Revision.date < c.match_date_out)

        if c.needle == "" and c.match_author == "" and c.match_ext == "" and\
                c.match_date_in == "" and c.match_date_out == "":
            c.found_files = []
            c.found_dirs = []
        else:
            c.found_files = file_q.all()
            if c.match_ext == "":
                c.found_dirs = dir_q.all()
            else:
                c.found_dirs = []

        return render('/derived/show/searchresults.html')


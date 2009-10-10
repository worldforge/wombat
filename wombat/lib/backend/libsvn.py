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
import pysvn
import os
import os.path
from datetime import datetime
from pylons import config
from wombat.model import Revision, Dir, File, Tag, Asset
from sqlalchemy.sql import func

def get_client():
    """()->pysvn.Client
    Get an initialized pysvn client object
    """
    client = pysvn.Client()
    client.exception_style = 1
    return client

def get_tag_from_path(session, path):
    """(Session, string)->Tag
    Get automated category tag from path
    """
    tag_name = "category_%s" % path[:path.find(os.path.sep)]
    tag = session.query(Tag).filter_by(name=tag_name).first()
    if tag is None:
        tag = Tag(tag_name)
    return tag

def get_tag_from_filetype(session, type):
    """(Session, string)->Tag
    Get automated type tag from filetype
    """
    type_name = "type_%s" % type
    tag = session.query(Tag).filter_by(name=type_name).first()
    if tag is None:
        tag = Tag(type_name)
    return tag

def get_create_revision(path, session, rev_id):
    """(string, Session, int)->Revision
    Fetch revision with id 'rev_id' from database or create a new entry.
    """
    revision = session.query(Revision).get(rev_id)
    if revision is None:
        # Need to create a new revision
        try:
            client = get_client()
            # We ask for one element, so only return one. pysvn.Client.log
            # always returns a list.
            log = client.log(path,
                    revision_start=pysvn.Revision(pysvn.opt_revision_kind.number, rev_id),
                    revision_end=pysvn.Revision(pysvn.opt_revision_kind.number, rev_id))[0]
            # We asked for revision by number here, so pysvn.revision.kind is
            # number, so asking for log.revision.number is safe here
            revision = Revision(log.revision.number, u"r%s" % log.revision.number,
                                unicode(log.message), unicode(log.author),
                                datetime.utcfromtimestamp(log.date))
            session.add(revision)
        except pysvn.ClientError, e:
            #TODO: Raise an error here
            return None

    return revision

def create_rev_entry(rev_path, session, rev=None, recurse=False):
    """(string, Session, Revision)-> none
    Create a database entry for a given (or the current) revision
    """
    if rev_path == u'':
        rev_path = u'.'

    if rev is None:
        pyrev = pysvn.Revision(pysvn.opt_revision_kind.head)
    else:
        pyrev = pysvn.Revision(pysvn.opt_revision_kind.number, rev.id)

    client = get_client()
    info_list = client.info2(rev_path, revision=pyrev, recurse=recurse)

    for path, info in info_list:
        if recurse:
            # For some reason, the top level dir is called trunk in the
            # recursive info, but paths under the top level dir don't contain
            # that part.
            if path != "trunk":
                path = unicode(path)
            else:
                path = u"."
        else:
            # restore the old path, client.info2 only has the top level name
            path = unicode(rev_path)

        if rev is None:
            revision = get_create_revision(path, session, info.last_changed_rev.number)
        else:
            revision = rev

        if revision is None:
            print "failed to find revision"
            continue

        if info.kind == pysvn.node_kind.dir:
            old_dir = session.query(Dir).get(path)
            if old_dir is not None:
                old_dir.revision = revision
                session.add(revision)
                continue
            # '.' does not look nice for the breadcrumb path
            if path == u".":
                dir_name = u"/"
            else:
                dir_name = unicode(os.path.basename(path))

            new_dir = Dir(path, dir_name, unicode(info.repos_root_URL))
            new_dir.revision = revision

            parent_path = unicode(os.path.dirname(path))
            # top level dirs have an empty parent, not "trunk", just to make
            # parsing more fun
            if parent_path == u"":
                parent_path = u"."
            parent_dir = session.query(Dir).get(parent_path)
            if parent_dir is not None and path != u".":
                new_dir.parent = parent_dir

            session.add(new_dir)
        elif info.kind == pysvn.node_kind.file:
            if not os.path.exists(path):
                continue
            old_file = session.query(File).get(unicode(path))
            if old_file is not None:
                old_file.size = os.path.getsize(path)
                old_file.revision = revision
                parent = old_file.directory
                while parent is not None:
                    parent.revision = revision
                    session.add(parent)
                    parent = parent.parent
                session.add(old_file)
                continue

            new_file = File(path, os.path.basename(path),
                            os.path.getsize(path), info.repos_root_URL)
            new_file.revision = revision

            parent_path = unicode(os.path.dirname(path))
            if parent_path == u'':
                parent_path = u'.'
            parent_dir = session.query(Dir).get(parent_path)
            if parent_dir is None:
                raise Exception("Rats, pysvn has the same problem with missing parent dirs")
            new_file.directory = parent_dir
            session.add(new_file)

            tags = []

            tags.append(get_tag_from_path(session, new_file.path))
            tags.append(get_tag_from_filetype(session, new_file.type))

            asset = session.query(Asset).filter(Asset.files.contains(new_file)).first()
            if asset is None:
                asset = Asset("auto_%s" % new_file.name, tags)
                asset.files.append(new_file)
                session.add(asset)

        else:
            raise Exception("Node type %s not handled" % info.kind)

        session.commit()

################################################
# Public functions

def add(path, session):
    """(string, session)->none
    Add a path to the version control backened
    """
    #TODO: Implement this
    raise Exception(NotImplemented)

def commit(paths, msg, userid, session):
    """([string], string, int, session)->none
    Commit a list of files to the version control
    """
    #TODO: implement this
    raise Exception(NotImplemented)

def fetch(globals):
    """({globals})->none
    Update the repository working copy.
    This is separate from updating the changes in the database, which is what
    update() does.
    """
    globals.update_status = "Fetching"
    # Store current working directory
    cwd = os.getcwd()

    os.chdir(config['app_conf']['media_dir'])
    client = get_client()
    try:
        revision = client.update(path='.', recurse=True)
        globals.update_status = "Updated to revision %s" % revision[0].number
    except pysvn.ClientError, e:
        globals.update_status = e.args[0]
    finally:
        # Last but not least, go back to whereever we were before
        os.chdir(cwd)

def scan(session):
    """(session)->none
    Do the initial scan of the media dir and create the database entries.
    """
    media_dir = config['app_conf']['media_dir']
    cwd = os.getcwd()
    os.chdir(media_dir)
    create_rev_entry(rev_path=".", session=session, recurse=True)
    os.chdir(cwd)

def update(session):
    """(session)->node
    Update the database entries to reflect the current status of the media dir
    """
    revision = session.query(func.max(Revision.id)).first()[0]
    cwd = os.getcwd()
    os.chdir(config['app_conf']['media_dir'])
    client = get_client()

    log = client.log(".", revision_start=pysvn.Revision(pysvn.opt_revision_kind.head),
                        revision_end=pysvn.Revision(pysvn.opt_revision_kind.number, revision+1),
                        discover_changed_paths=True)

    log.reverse()
    for entry in log:
        if entry.revision.number == revision:
            continue
        revision = Revision(entry.revision.number, u"r%s" % entry.revision.number,
                        unicode(entry.message), unicode(entry.author),
                        datetime.utcfromtimestamp(entry.date))
        session.add(revision)

        # Unfortunately the changed paths are not sorted, so in order to keep
        # the database sane, we will go over the list directories first, files
        # second.
        for path in entry.changed_paths:
            stripped_path = path.path.lstrip("%strunk%s" % (os.sep, os.sep))
            if os.path.isdir(stripped_path):
                if path.action in ("A", "M"):
                    create_rev_entry(rev_path=stripped_path, session=session,
                                     rev=revision, recurse=False)
                elif path.action == "D":
                    del_dir = session.query(Dir).get(unicode(stripped_path))
                    if del_dir is not None:
                        session.delete(del_dir)
                        session.commit()

        for path in entry.changed_paths:
            stripped_path = path.path.lstrip("%strunk%s" % (os.sep, os.sep))
            if os.path.isfile(stripped_path):
                if path.action in ("A", "M"):
                    create_rev_entry(rev_path=stripped_path, session=session,
                                     rev=revision, recurse=False)
                elif path.action == "D":
                    del_file = session.query(File).get(unicode(stripped_path))
                    if del_file is not None:
                        session.delete(del_file)
                        session.commit()

    os.chdir(cwd)



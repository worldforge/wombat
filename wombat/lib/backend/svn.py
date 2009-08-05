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

import os.path
from subprocess import Popen, PIPE
from pylons import config
from wombat.model import Revision, File, Dir, Asset, Tag, User
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.sql import func
from svn_xml_parser import parse_svn
from wombat.lib.sanitation import escape_quote, check_quote

def get_tag_from_path(session, path):
    tag_name = "category_%s" % path[:path.find(os.path.sep)]
    tag = session.query(Tag).filter_by(name=tag_name).first()
    if tag is None:
        tag = Tag(tag_name)
    return tag

def get_tag_from_filetype(session, type):
    type_name = "type_%s" % type
    tag = session.query(Tag).filter_by(name=type_name).first()
    if tag is None:
        tag = Tag(type_name)
    return tag

def call_svn_cmd(path, cmd, opts):
    """string, string, string -> string
    Call a svn command and return an xml string
    """
    stringlist = []
    cli_out = Popen("svn %s %s '%s' 2> /dev/null" % (cmd, opts, path), shell=True,
                    stdout=PIPE, close_fds=True).stdout
    try:
        stringlist = cli_out.readlines()
        xml_string = "".join(stringlist)
        return xml_string
    except:
        return None

def get_create_revision(path, session, rev_id):
    """string, Session, int -> Revision
    Fetch revision with id 'rev_id' from database or create a new entry.
    """
    revision = session.query(Revision).get(rev_id)
    if revision is None:
        xml_string = call_svn_cmd(path, "log", "--incremental --xml -r %s" % rev_id)
        if xml_string == "":
            return None
        svn = parse_svn(xml_string)
        revision = Revision(svn.revision, u"r%s" % svn.revision, svn.msg, svn.author, svn.date)
        session.add(revision)

    return revision

def create_rev_entry(rev_path, session, rev=None):
    """string, Session -> None
    Generate a database entry.
    """
    if rev_path == u'':
        rev_path = u'.'

    if not os.path.exists(rev_path):
        return

    if rev is not None:
        xml_string = call_svn_cmd(rev_path, "info", "--incremental --xml -r %s" % rev.id)
    else:
        xml_string = call_svn_cmd(rev_path, "info", "--incremental --xml")

    svn = parse_svn(xml_string)

    if rev is None:
        revision = get_create_revision(rev_path, session, svn.revision)
    else:
        revision = rev

    if revision is None:
        return

    if svn.kind == u"file":
        old_file = session.query(File).get(unicode(rev_path))
        if old_file is not None:
            old_file.size = os.path.getsize(rev_path)
            old_file.revision = revision
            parent = old_file.directory
            while parent is not None:
                parent.revision = revision
                session.add(parent)
                parent = parent.parent
            session.add(old_file)
            return

        new_file = File(rev_path, os.path.basename(rev_path),
                os.path.getsize(rev_path), svn.root)
        new_file.revision = revision
        session.add(new_file)

        parent_path = os.path.dirname(rev_path)
        if parent_path == u'':
            parent_path = u'.'
        parent_dir = session.query(Dir).get(parent_path)
        if parent_dir is None:
            # Parent directory was probably created in the same commit.
            # Recurse just to make sure the parent dir exits. This is
            # sub-optimal performance-wise, but keeps the database consistent.
            # SVN XML sucks.
            create_rev_entry(parent_path, session, rev)
            parent_dir = session.query(Dir).get(parent_path)

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

    elif svn.kind == u"dir":
        old_dir = session.query(Dir).get(unicode(rev_path))
        if old_dir is not None:
            old_dir.revision = revision
            session.add(revision)
            return

        if rev_path != u'.':
            dir_name = os.path.basename(rev_path)
        else:
            dir_name = u'/'
        new_dir = Dir(rev_path, dir_name, svn.root)
        new_dir.revision = revision

        parent_path = os.path.dirname(rev_path)
        if parent_path == u'':
            parent_path = u'.'
        parent_dir = session.query(Dir).get(parent_path)
        if parent_dir is not None and rev_path != u'.':
            new_dir.parent = parent_dir
        session.add(new_dir)

def scan(session):
    """Session -> None
    Iterate over the media dir and generate database entries
    """
    media_dir = config['app_conf']['media_dir']
    cwd = os.getcwd()
    os.chdir(media_dir)
    for root, dirs, files in os.walk(media_dir):
        new_root = unicode(root.replace(media_dir,'').lstrip('/'))
        create_rev_entry(new_root, session)
        for file in files:
            file_path = os.path.join(new_root, file)
            create_rev_entry(file_path, session)

        if ".svn" in dirs:
            dirs.remove(".svn")
    session.commit()
    os.chdir(cwd)

def delete_file_entry(rev_path, session):
    """string, Session -> None
    Delete a file entry
    """
    del_file = session.query(File).get(rev_path)
    if del_file is not None:
        session.delete(del_file)

def update_rev(session, rev_id):
    """Session, int -> None
    Update a revision entry
    """
    xml_string = call_svn_cmd(".", "log", "--incremental --xml -v -r %s" % rev_id)
    svn = parse_svn(xml_string)
    revision = Revision(svn.revision, u"r%s" % svn.revision, svn.msg, svn.author, svn.date)
    session.add(revision)

    # reverse the order of the changed paths, as svn info --xml reverses them as
    # well. This way we don't add files before adding the parent dir.
    svn.changed_paths.reverse()

    for action, path in svn.changed_paths:
        if action in (u'M', u'A'):
            create_rev_entry(path, session, revision)
        elif action in (u'D'):
            delete_file_entry(path, session)
        else:
            continue

def update(session):
    """Session -> None
    Update to latest svn revision if needed
    """
    revision = session.query(func.max(Revision.id)).first()[0]
    cwd = os.getcwd()
    os.chdir(config['app_conf']['media_dir'])
    xml_string = call_svn_cmd(".", "info", "--incremental --xml")
    svn = parse_svn(xml_string)
    while revision < svn.revision:
        revision += 1
        update_rev(session, revision)
    session.commit()
    os.chdir(cwd)

def fetch(globals):
    from threading import Timer
    globals.update_status = "Fetching"
    cwd = os.getcwd()
    os.chdir(config['app_conf']['media_dir'])
    ret = call_svn_cmd(".", "update", "--non-interactive")
    if ret:
        globals.update_status = ret
    else:
        globals.update_status = "Fetching failed"

def add(path, session):
    #svn add (File or dir)
    #add to the db
    cwd = os.getcwd()
    media_dir = config['app_conf']['media_dir']
    os.chdir(media_dir)
    pipe = os.popen("svn add '%s'" % path)
    rc = pipe.close()
    if  rc != None and rc % 256:
        return "There were some errors"
    os.chdir(cwd)

def commit(paths, message, userid, session):
    #svn commit (File or dir)
    cwd = os.getcwd()
    media_dir = config['app_conf']['media_dir']
    os.chdir(media_dir)
    user = session.query(User).get(userid)
    message = escape_quote(message)
    #TODO error handling
    if user.user_data.vcs_user is not None:
        username = user.user_data.vcs_user
        password = user.user_data.vcs_pass
        if check_quote(username) and check_quote(password):
            return "Quotes are not allowed for now"
        pipe = os.popen("svn commit -m '%s' --username '%s' --password '%s'" % (message, username, password))
        rc = pipe.close()
        if  rc != None and rc % 256:
            return "There were some errors"
    elif config['app_conf']['default_vcs'] == "true":
        default_vcs_user = config['app_conf']['default_vcs_user']
        default_vcs_pass = config['app_conf']['default_vcs_pass']
        if check_quote(default_vcs_user) and check_quote(default_vcs_pass):
            return "Quotes are not allowed for now"
        pipe = os.popen("svn commit -m '%s' --username '%s' --password '%s'" % (message, default_vcs_user, default_vcs_pass))
        rc = pipe.close()
        if  rc != None and rc % 256:
            return "There were some errors"
    else:
        #Trying anyway
        pipe = os.popen("svn commit -m '%s'" % message)
        rc = pipe.close()
        if  rc != None and rc % 256:
            return "There were some errors"

    for path in paths:
        create_rev_entry(path, session)
    session.commit()
    os.chdir(cwd)

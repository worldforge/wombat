"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import os.path
import string
from time import strptime, mktime
from rev_info import Info
from preview import getThumbnail, getIcon
from filetypes import getType, img_inline

def getBreadcrumbTrail(dir):
    trail = []
    while dir.parent is not None:
        trail.append(dir.parent)
        dir = dir.parent

    trail.reverse()
    return trail

def canScan(session):
    from wombat.model import Revision
    if session.query(Revision).first() is not None:
        return False
    return True

def createTextPreview(file):
    open_tags = """\
                        <div id="textmedia">
                            <pre>
"""
    close_tags = """\
                            </pre>
                        </div>
"""
    try:
        f = open(os.path.join(config['app_conf']['media_dir'], file.path), 'r')
        content = u"".join(f.readlines())
        f.close()
    except UnicodeDecodeError:
        content = "Error converting %s to unicode" %file.name
        f.close()
    except:
        content = "Error reading %s" % file.name
    return (open_tags, content, close_tags)

def createImagePreview(file):
    open_tags = """\
                        <div id="media">
"""
    base, ext = os.path.splitext(file.name)
    if ext in img_inline:
        content = """\
                            <a href="/media/%s"><img src="%s" alt="%s" border="0"/></a>
""" % (file.path, getThumbnail(file), file.name)
    else:
        content = """\
                            Sorry, but %s files cannot be rendered inline.
""" % ext
    close_tags = """\
                        </div>
"""
    return (open_tags, content, close_tags)

def createSoundPreview(file):
    open_tags = """\
                        <div id="media">
"""
    content = """\
                            <embed src="/media/%s" controller="true" autoplay="false"
                            autostart="false" height="40" width="250" loop="false" />
""" % file.path
    close_tags = """\
                        </div>
"""
    return (open_tags, content, close_tags)

def createPreview(file):
    type = getType(file.name)
    if type == "text":
        return createTextPreview(file)
    elif type == "image":
        return createImagePreview(file)
    elif type == "sound":
        return createSoundPreview(file)
    else:
        return ("", "Sorry, no preview for %s files available" % type, "")

def getLatestAdditions(session, num=5):
    from wombat.model import Revision
    rev = session.query(Revision).from_statement("SELECT * FROM revisions WHERE id = (SELECT MAX(revisions.id) FROM revisions)").first()
    if rev is None:
        return []
    return rev.files[:num]

def dateStrToEpoch(date_str):
    """dateStrToEpoch(string) -> float
    Convert an iso date string to seconds since epoch
    Returns seconds since epoch or 0 on error.
    """

    try:
        tm = strptime(date_str, "%Y-%m-%d")
        time = mktime(tm)
    except ValueError:
        try:
            tm = strptime(date_str, "%Y-%m-%d %H:%M:%S")
            time = mktime(tm)
        except ValueError:
            time = 0
    return time

def sorted_options_for_select(container, selected=None):
    """container(list, tuple, dict), string -> string
    Sorted version of the builtin function
    """
    return rails.options_for_select(sorted(container), selected)

def getAuthors(session):
    """Session -> [string]
    Get the list of authors
    """
    from sqlalchemy.sql import select
    from wombat.model import Revision

    authors = []
    authors_s = session.execute(select([Revision.author], distinct=True)).fetchall()

    for author in authors_s:
        authors.append(author[0])

    return authors

def getExtensions(session):
    """Session -> [string]
    Get the list of extensions
    """
    from sqlalchemy.sql import select
    from wombat.model import File

    exts = []
    exts_s = session.execute(select([File.ext], distinct=True)).fetchall()

    for ext in exts_s:
        exts.append(ext[0])

    return exts


def sizeToStr(size):
    """int -> string
    Create a human readable size string from byte size
    """
    size_name = ['B', 'kB', 'MB', 'GB']
    i = 0
    while size > 1024 and i < len(size_name):
        size /= 1024.0
        i += 1
    return "%.2f %s" % (size, size_name[i])

def truncStr(orig_str, max_len):
    """string, int -> string
    Truncate a string to the given length, with middle ellipsis.
    """
    if max_len == 0 or len(orig_str) < max_len:
        return orig_str

    trunc_len = (max_len-3)/2
    trunc_str = "%s...%s" % (orig_str[:trunc_len], orig_str[-trunc_len:])
    return trunc_str

def getCurrentUser(session, db_session):
    """
    Get the current logged in user
    """
    from wombat.model import User
    if 'user' in session:
        return db_session.query(User).get(session['user'])
    return None

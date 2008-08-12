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
from preview import getThumbnail
from json import assetToJson, assetListToJson

img_inline = ['.gif', '.jpg', '.png']
image_exts = ['.bmp', '.gif', '.ico', '.jpg', '.png', '.psd',
        '.psp','.pspimage', '.psptube', '.raw', '.svg', '.tga', '.tif', '.xcf']
model_exts = ['.3dc', '.3ds', '.blend', '.caf', '.cal', '.cmf', '.crf', '.csf',
        '.dxf', '.emdl', '.lwo', '.max', '.md3', '.mdl', '.mesh', '.mtl',
        '.ndo', '.obj', '.skeleton', '.srf', '.texture', '.wings', '.wrl',
        '.xaf', '.xmf', '.xrl', '.xsf', '.xsi']
sound_exts = ['.mid', '.mp3', '.ogg', '.wav']
text_exts = ['.asm', '.bat', '.cfg', '.cg', '.conf', '.glsl', '.hlsl','.htm',
        '.html', '.ini', '.material', '.txt', '.url', '.xml']

def getBreadcrumbTrail(rootdir, obj):
    trail = []
    if rootdir == obj or rootdir is None:
        return []
    dir_str = os.path.dirname(obj.getPath())
    dir_trail = string.split(dir_str, os.path.sep)
    entry_str = ""
    trail.append(rootdir)
    for entry in dir_trail:
        entry_str = os.path.join(entry_str, entry)
        if entry_str == "":
            continue
        dir = rootdir.getDir(entry_str)
        trail.append(dir)

    return trail

def canScan():
    if os.path.exists(config['app_conf']['scan_lock']):
        return False
    return True

def createScanLock():
    f = open(config['app_conf']['scan_lock'], 'w')
    f.close()

def createTextPreview(file):
    open_tags = """\
                        <div id="textmedia">
                            <pre>
"""
    close_tags = """\
                            </pre>
                        </div>
"""
    f = open(os.path.join(config['app_conf']['media_dir'], file.path), 'r')
    try:
        content = u"".join(f.readlines())
    except UnicodeDecodeError:
        content = "Error converting %s to unicode" %file.name
    except:
        content = "Error reading %s" % file.name

    f.close()
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

def getType(name):
    """
    """
    base, ext = os.path.splitext(name)
    ext = ext.lower()

    if ext in image_exts:
        type = "image"
    elif ext in model_exts:
        type = "model"
    elif ext in sound_exts:
        type = "sound"
    elif ext in text_exts:
        type = "text"
    else:
        type = "other"

    return type

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

def search(root_dir, needle, author, extension, date_in=0, date_out=0):
    """search
    """
    dirs, files = root_dir.search(needle, author, extension, date_in, date_out)
    return "{dirs: %s, files: %s}" % (assetListToJson(dirs), assetListToJson(files))

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


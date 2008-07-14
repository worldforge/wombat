"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import os.path
import string
from rev_info import Info
from preview import getThumbnail

img_inline = ['.gif', '.jpg', '.png']

def getBreadcrumbTrail(rootdir, obj):
    trail = []
    if rootdir == obj:
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
    if not os.path.exists(config['app_conf']['rootdir_cache']):
        return True

    if os.path.exists(config['app_conf']['scan_lock']):
        return False
    return True

def createScanLock():
    f = open(config['app_conf']['scan_lock'], 'w')
    f.close()

def createTextPreview(file):
    open_tags = """\
                        <div id="media">
                            <pre>
"""
    close_tags = """\
                            </pre>
                        </div>
"""
    f = open(file.getFullPath(), 'r')
    try:
        content = u"".join(f.readlines())
    except UnicodeDecodeError:
        content = "Error converting %s to unicode" %file.getName()
    except:
        content = "Error reading %s" % file.getName()

    f.close()
    return (open_tags, content, close_tags)

def createImagePreview(file):
    open_tags = """\
                        <div id="media">
"""
    ext = file.getExtension()
    if ext in img_inline:
        content = """\
                            <img src="%s" alt="%s" />
""" % (getThumbnail(file), file.getName())
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
""" % file.getPath()
    close_tags = """\
                        </div>
"""
    return (open_tags, content, close_tags)

def createPreview(file):
    type = file.getType()
    if type == "text":
        return createTextPreview(file)
    elif type == "image":
        return createImagePreview(file)
    elif type == "sound":
        return createSoundPreview(file)
    else:
        return ("", "Sorry, no preview for %s files available" % type, "")

def getInfo(path):
    """string -> Info
    Get an Info object for path
    """
    info = Info()
    info.load(path)
    return info

def getRevision():
    info = getInfo("")
    return info.getRevision()

def getMostPopularFile(root_dir):
    """RootDir -> string
    Get the most popular file ext and count from the root dir and format to a
    nice string output
    """
    return "%s (%s)" % root_dir.getMostPopularFile()

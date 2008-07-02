"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import os.path
import string

def getBreadcrumbTrail(rootdir, obj):
    trail = []
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


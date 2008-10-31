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

import md5
import os.path
from pylons import config
from filetypes import getType

thumb_size = (128, 128)
icon_size = (32, 32)

def loadPreview(file, type):
    """loadPreview(File, string) -> string
    Load a preview from thumb_dir.
    Returns the path to the preview file or None if the file doesn't exist.
    """
    hash = md5.new(file.path)
    base, ext = os.path.splitext(file.name)
    thumb_name = "%s_%s%s" % (hash.hexdigest(), type, ext)
    thumb_path = os.path.join(config['app_conf']['thumb_dir'], thumb_name)
    if not os.path.exists(thumb_path):
        return None
    else:
        return thumb_name

def createPreview(file, type):
    """createPreview(File, string) -> string
    Create a preview file.
    Return the preview file name or None on error.
    """
    hash = md5.new(file.path)
    base, ext = os.path.splitext(file.name)

    if type == "thumb":
        size = thumb_size
        format = (255,255,255,0)
    elif type == "icon":
        size = icon_size
        format = (255,255,255,255)
        ext = ".png"
    else:
        return None

    thumb_name = "%s_%s%s" % (hash.hexdigest(), type, ext)
    thumb_path = os.path.join(config['app_conf']['thumb_dir'], thumb_name)
    if not os.path.exists(config['app_conf']['thumb_dir']):
        try:
            os.mkdir(config['app_conf']['thumb_dir'])
        except OSError:
            return None


    try:
        from PIL import Image

        temp_image = Image.open(os.path.join(config['app_conf']['media_dir'], file.path))
        temp_image.thumbnail(size, Image.ANTIALIAS)
        thumb_image = Image.new("RGBA", size, format)
        offset = (int((size[0] - temp_image.size[0]) / 2.0) ,
                int((size[1] - temp_image.size[1]) / 2.0))
        thumb_image.paste(temp_image, offset)
        thumb_image.save(thumb_path)

        return thumb_name
    except ImportError:
        return None
    except IOError:
        return None
    except OverflowError:
        return None

def getThumbnail(file):
    """getThumbnail(File) -> string
    If needed, generates a thumbnail and saves it to the thumb_dir.
    Returns the path to the thumbnail file.
    """
    thumb_name = loadPreview(file, "thumb")
    if thumb_name == None:
        thumb_name = createPreview(file, "thumb")
        if thumb_name == None:
            return "/media/%s" % file.path

    return "/thumb/%s" % thumb_name

def getIcon(file):
    """getIcon(File) -> string
    If needed, generates an icon and saves it to the thumb_dir
    Returns the path to the icon file.
    """
    icon_name = loadPreview(file, "icon")
    if icon_name == None:
        icon_name = createPreview(file, "icon")
        if icon_name == None:
            return "/images/%s.png" % getType(file.name)

    return "/thumb/%s" % icon_name


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
from PIL import Image
from pylons import config

size = (128, 128)

def loadThumbnail(file):
    """loadThumbnail(File) -> string
    Load a thumbnail from thumb_dir.
    Returns the path to the thumbnail file or None if the file doesn't exist.
    """
    hash = md5.new(file.getPath())
    thumb_name = "%s_thumb%s" % (hash.hexdigest(), file.getExtension())
    thumb_path = os.path.join(config['app_conf']['thumb_dir'], thumb_name)
    if not os.path.exists(thumb_path):
        return None
    else:
        return thumb_name

def createThumbnail(file):
    """createThumbnail(File) -> string
    Create a thumbnail file.
    Return the thumbnail file name or None on error.
    """
    hash = md5.new(file.getPath())
    thumb_name = "%s_thumb%s" % (hash.hexdigest(), file.getExtension())
    thumb_path = os.path.join(config['app_conf']['thumb_dir'], thumb_name)
    if not os.path.exists(config['app_conf']['thumb_dir']):
        try:
            os.mkdir(config['app_conf']['thumb_dir'])
        except OSError:
            return None

    temp_image = Image.open(file.getFullPath())
    temp_image.thumbnail(size, Image.ANTIALIAS)
    thumb_image = Image.new("RGBA", size, (255,255,255,0))
    offset = (int((size[0] - temp_image.size[0]) / 2.0) ,
            int((size[1] - temp_image.size[1]) / 2.0))
    thumb_image.paste(temp_image, offset)
    thumb_image.save(thumb_path)

    return thumb_name

def getThumbnail(file):
    """getThumbnail(File) -> string
    If needed, generates a thumbnail and saves it to the thumb_dir.
    Returns the path to the thumbnail file.
    """
    thumb_name = loadThumbnail(file)
    if thumb_name == None:
        thumb_name = createThumbnail(file)
        if thumb_name == None:
            return "/media/%s" % file.getPath()

    return "/thumb/%s" % thumb_name

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

from os.path import getsize, join, basename, getmtime, splitext
from time import strftime, gmtime
from pylons import config

image_exts = ['.png', '.jpg', '.gif', '.bmp', '.tiff']
model_exts = ['.md3', '.blend', '.cal', '.caf', '.mesh', '.xml', '.wrl',
        '.skeleton', '.max', '.3ds']
sound_exts = ['.wav', '.mp3', '.ogg']
text_exts = ['.txt', '.html']

class File:
    def __init__(self, path):
        """__init__(path) -> File object
        Called while the RootDir object is scanning the repository.
        All time-consuming operations should happen here.
        """
        self.path = path
        self.fullpath = join(config['app_conf']['media_dir'], path)
        self.size = getsize(self.fullpath)
        self.mtime = getmtime(self.fullpath)
        name,ext = splitext(basename(path))
        ext = ext.lower()
        if ext in image_exts:
            self.type = "image"
        elif ext in model_exts:
            self.type = "model"
        elif ext in sound_exts:
            self.type = "sound"
        elif ext in text_exts:
            self.type = "text"
        else:
            self.type = "other"

    def getPath(self):
        """getPath() -> string
        Get the file's path within the media dir
        """
        return self.path

    def getFullPath(self):
        """getFullPath() -> string
        Get the file's file full file system path
        """
        return self.fullpath

    def getName(self):
        """getName() -> string
        Get the file's name
        """
        return basename(self.path)

    def getSize(self):
        """getSize() -> int
        Get the file's size in bytes
        """
        return self.size

    def getPrettySize(self):
        """getPrettySize() -> string
        Get the file's size as nice string with the byte count converted to the
        correct magnitude.
        i.e. 1024 byte will be 1 kB.
        """
        size = self.size
        i = 0
        size_name = ['B', 'kB', 'MB', 'GB']
        while size > 1024 and i < len(size_name):
            size /= 1024.0
            i += 1
        return "%.2f %s" % (size, size_name[i])

    def getType(self):
        """getType() -> string
        Get the file's type
        """
        return self.type

    def getMtime(self):
        """getMtime() -> int
        Get the file's last modification time in secons from epoch.
        """
        return self.mtime

    def getLastChanged(self):
        """getLastChanged() -> string
        Get a pretty string-formatted version of the file's mtime
        """
        return strftime("%Y-%m-%d %H:%M:%S %Z", gmtime(self.mtime))


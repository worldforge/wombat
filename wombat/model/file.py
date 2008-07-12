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

from os.path import getsize, join, basename, splitext
from time import strptime, mktime
from pylons import config
from wombat.lib.helpers import getInfo
import mimetypes

image_exts = ['.bmp', '.gif', '.ico', '.jpg', '.png', '.psd', '.psp',
        '.pspimage', '.psptube', '.raw', '.svg', '.tga', '.tif', '.xcf']
model_exts = ['.3dc', '.3ds', '.blend', '.caf', '.cal', '.crf', '.csf', '.dxf',
        '.emdl', '.lwo', '.max', '.md3', '.mdl', '.mesh', '.mtl', '.ndo',
        '.obj', '.skeleton', '.srf', '.texture', '.wings', '.wrl', '.xaf',
        '.xmf', '.xrl', '.xsf', '.xsi']
sound_exts = ['.mid', '.mp3', '.ogg', '.wav']
text_exts = ['.asm', '.bat', '.cfg', '.cg', '.conf', '.glsl', '.hlsl',
        '.htm', '.html', '.ini', '.material', '.txt', '.url', '.xml']

class File:
    def __init__(self, path):
        """__init__(path) -> File object
        Called while the RootDir object is scanning the repository.
        All time-consuming operations should happen here.
        """
        self.path = path
        self.fullpath = join(config['app_conf']['media_dir'], path)
        self.size = getsize(self.fullpath)
        self.setType()
        self.setInfo()

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

    def setType(self):
        """setType() -> None
        Set the file's type
        """
        name,ext = splitext(basename(self.path))
        ext = ext.lower()
        self.extension = ext
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

    def getType(self):
        """getType() -> string
        Get the file's type
        """
        return self.type

    def getExtension(self):
        """None -> string
        Get the file's extension
        """
        return self.extension

    def getMtime(self):
        """getMtime() -> int
        Get the file's last modification time in secons from epoch.
        """
        return self.mtime

    def setInfo(self):
        """setSvnInfo() -> None
        Set the NodeInfo for the file
        """
        self.info = getInfo(self.path)

        format = "%Y-%m-%d %H:%M:%S"
        time_list = self.info.date.split(" ")
        if len(time_list) < 2:
            self.mtime = 0
            return

        time_str = " ".join(time_list[:2])
        try:
            time_ofs = time_list[2]
        except IndexError:
            time_ofs = "+0000"

        try:
            tm = strptime(time_str, format)
        except ValueError:
            self.mtime = 0
            return
        self.mtime = mktime(tm)

        if len(time_ofs) < 5:
            time_ofs = "+0000"

        try:
            ofs_hours = int(time_ofs[1:3])
        except ValueError:
            ofs_hours = 0
        try:
            ofs_minutes = int(time_ofs[3:5])
        except ValueError:
            ofs_minutes = 0

        ofs_seconds = ((ofs_hours * 60) + ofs_minutes) * 60

        if time_ofs[0] == "+":
            self.mtime += ofs_seconds
        else:
            self.mtime -= ofs_seconds

    def getRevision(self):
        """None -> string
        Get the revision of the file
        """
        return self.info.getRevision()

    def getAuthor(self):
        """None -> string
        Get the author of the last change
        """
        return self.info.getAuthor()

    def getDate(self):
        """None -> string
        Get the date/time of the last change
        """
        return self.info.getDate()

    def getLog(self):
        """None -> string
        Get the log message of the last change
        """
        return self.info.getLog()

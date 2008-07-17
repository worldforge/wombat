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

from os.path import basename, join
from pylons import config
from wombat.lib.helpers import getInfo
from time import strptime, mktime

class Dir:
    """A Directory abstraction
    This class will cache all information needed about a directory.
    """

    def __init__(self, path):
        """__init__(path) -> Dir object
        Called while the RootDir object is scanning the repository, the
        initialization function should perform all time-consuming operations.
        """
        self.subdirs = []
        self.files = []
        self.path = path
        self.full_path = join(config['app_conf']['media_dir'], path)
        self.setInfo()

    def addSubdir(self, dir):
        """addSubdir(dir) -> None
        Add a Dir object as subdirectory
        """
        self.subdirs.append(dir)

    def getSubdirs(self):
        """getSubdir() -> List of subdirectories
        Get a list of subdirectories.
        """
        return self.subdirs

    def addFile(self, file):
        """addFile(file) -> None
        Add a File object to the list of files
        """
        self.files.append(file)

    def getFiles(self):
        """getFiles() -> List of files
        Get a list of files contained in the current directory
        """
        return self.files

    def getFilesByType(self, file_list=[]):
        """getFilesByType() -> (images, models, sounds, texts, others)
        Get a tuple containing a list of image, model, sound, text and other
        files, in this order.
        """
        image_files = []
        model_files = []
        sound_files = []
        text_files = []
        other_files = []

        if file_list == []:
            file_list = self.files

        for file in file_list:
            type = file.getType()
            if type == "image":
                image_files.append(file)
            elif type == "model":
                model_files.append(file)
            elif type == "sound":
                sound_files.append(file)
            elif type == "text":
                text_files.append(file)
            else:
                other_files.append(file)

        return (image_files, model_files, sound_files, text_files, other_files)

    def getPath(self):
        """getPath() -> string
        Get the directory's path in the media repo
        """
        return self.path

    def getFullPath(self):
        """getFullPath() -> string
        Get the full path of the directory
        """
        return self.full_path

    def getName(self, max_len=0):
        """getName(int) -> string
        Get the name of the directory
        """
        name = basename(self.path)
        if max_len == 0 or len(name) < max_len:
            return name

        trunc_len = (max_len-3)/2
        trunc_name = "%s...%s" % (name[:trunc_len], name[-trunc_len:])
        return trunc_name

    def getType(self):
        """getType() -> string
        Get the object's type
        """
        return "dir"

    def setInfo(self):
        """setSvnInfo() -> None
        Initialize the NodeInfo for the directory
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

    def getMtime(self):
        """None -> float
        Get the seconds since epoch of the last change
        """
        return self.mtime

    def getLog(self):
        """None -> string
        Get the log message of the last change
        """
        return self.info.getLog()

    def getRepoUrl(self):
        """None -> string
        Get the URL of the parent repository
        """
        return self.info.getRepoUrl()

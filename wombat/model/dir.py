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
from wombat.lib.svnwrap import getSvnInfo, SvnInfo

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
        self.setSvnInfo()

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

    def getFilesByType(self):
        """getFilesByType() -> (images, models, sounds, texts, others)
        Get a tuple containing a list of image, model, sound, text and other
        files, in this order.
        """
        image_files = []
        model_files = []
        sound_files = []
        text_files = []
        other_files = []

        for file in self.files:
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

    def getName(self):
        """getName() -> string
        Get the name of the directory
        """
        return basename(self.path)

    def getType(self):
        """getType() -> string
        Get the object's type
        """
        return "dir"

    def setSvnInfo(self):
        """setSvnInfo() -> None
        Set the Svn Info from the repository
        """
        self.svn_info = getSvnInfo(self.path)

    def getRev(self):
        """getRev() -> int
        Get the svn revision of the file
        """
        return self.svn_info.getRev()

    def getLastChangedAuthor(self):
        """getLastChangedAuthor(self) -> string
        Get the author of the last change
        """
        return self.svn_info.getLastChangeAuthor()

    def getLastChangedRev(self):
        """getLastChangedRev(self) -> string
        Get the revision of the last change.
        """
        return self.svn_info.getLastChangeRev()

    def getLastChangedDate(self):
        """getLastChanged() -> string
        Get the date/time of the last change
        """
        return self.svn_info.getLastChangeDate()


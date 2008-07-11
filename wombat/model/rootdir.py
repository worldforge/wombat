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

import os
import os.path

from pylons import config

from wombat.model.file import File
from wombat.model.dir import Dir

def cmpRev(file_x, file_y):
    """cmpRev(x,y) -> -1,0,1
    Compare the revision of x with the revision of y.
    If x is newer than y, return -1.
    Used as argument for sort, this will make the most recently updated files go first.
    """
    try:
        x = int(file_x.getRevision())
    except ValueError:
        x = 0
    try:
        y = int(file_y.getRevision())
    except ValueError:
        y = 0
    if x > y:
        return -1
    elif x == y:
        return 0
    else:
        return 1

def cmpLatest(file_x, file_y):
    """cmpLatest(x,y) -> -1,0,1
    Compare mtime of x with the mtime of y.
    If x is newer than y, return -1.
    Used as argument for sort, this will make the latest files go first.
    """
    x = file_x.getMtime()
    y = file_y.getMtime()
    if x > y:
        return -1
    elif x == y:
        return 0
    else:
        return 1

class RootDir(Dir):
    """RootDir
    A special Dir object living at the root of the media repository.
    It takes care of keeping lists of all files and directories, scanning the
    repository, etc.
    """
    def __init__(self, path):
        """__init__(path) -> RootDir object
        Initialize the root dir
        """
        Dir.__init__(self, path)
        self.path = ""
        self.all_dirs = {}
        self.all_files = {}
        self.scanpath = path
        self.latest = []
        self.authors = {}
        self.setInfo()

    def getName(self):
        """getName() -> string
        Always returns "/"
        """
        return "/"

    def addDir(self, dir):
        """addDir(dir) -> None
        Add a Dir object to the list of all directories
        """
        self.all_dirs[dir.path] = dir

    def addAuthor(self, obj):
        """File -> None
        Add file to the files by author dict
        """
        author = obj.getAuthor()
        if not self.authors.has_key(author):
            self.authors[author] = ([], [])

        if obj.type == "dir":
            self.authors[author][0].append(obj)
        else:
            self.authors[author][1].append(obj)

    def getAuthorDict(self):
        """None -> {string:([Dir], [File])}
        Get a dict containing authors and the files they changed.
        """
        return self.authors

    def getAuthors(self):
        """None -> [string]
        Get a list of authors.
        """
        return self.authors.keys()

    def getDir(self, path):
        """getDir(path) -> Dir
        Get the directory at "path"
        Raises KeyError if the directory doesn't exist.
        """
        return self.all_dirs[path]

    def addGlobalFile(self, file):
        """addGlobalFile(file) -> None
        Add a File object to the list of all files
        """
        self.all_files[file.path] = file

    def getFile(self, path):
        """getFile(path) -> File
        Get the file at "path"
        Raises KeyError if the file doesn't exist.
        """
        return self.all_files[path]

    def scan(self):
        """scan() -> None
        Scan the media repository for files and directories, adding them to the
        respective data structures as we go.
        This can take a long time
        """
        # First, add self to the all_dirs dict
        self.addDir(self)

        for root, dirs, files in os.walk(self.scanpath):
            new_root = root.replace(config['app_conf']['media_dir'],'').lstrip('/')
            parent_dir = self.getDir(new_root)
            for file in files:
                file_path = os.path.join(new_root, file)
                file_obj = File(file_path)
                parent_dir.addFile(file_obj)
                self.addGlobalFile(file_obj)
                self.addAuthor(file_obj)

            #TODO: This should probably be done nicer.
            if ".svn" in dirs:
                dirs.remove(".svn")

            for dir in dirs:
                dir_path = os.path.join(new_root, dir)
                dir_obj = Dir(dir_path)
                parent_dir.addSubdir(dir_obj)
                self.addDir(dir_obj)

        self.latest = self.all_files.values()
        self.latest.sort(cmp=cmpRev)

    def getLatestAdditions(self, num=5):
        """getLatestAdditions(num=5) -> [files]
        Get the num files most recently added/changed.
        """
        return self.latest[:num]

    def search(self, needle, author):
        """search(needle, author) -> ([dirs],[files])
        Search for files and directories containing the string in needle in
        their name. Returns a tuple with a list of directory and file matches.
        """
        dirs = []
        files = []

        if needle == "":
            author_dict = self.getAuthorDict()
            if author == "" or not author_dict.has_key(author):
                return ([], [])
            return author_dict[author]

        for key in self.all_dirs.keys():
            d_name = os.path.basename(key)
            if d_name.find(needle) < 0:
                continue
            if author == "" or author == self.all_dirs[key].getAuthor():
                dirs.append(self.all_dirs[key])

        for key in self.all_files.keys():
            f_name = os.path.basename(key)
            if f_name.find(needle) < 0:
                continue
            if author == "" or author == self.all_files[key].getAuthor():
                files.append(self.all_files[key])

        return (dirs, files)


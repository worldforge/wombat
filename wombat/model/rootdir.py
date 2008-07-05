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

def cmpLatest(file_x, file_y):
    x = file_x.getMtime()
    y = file_y.getMtime()
    if x > y:
        return -1
    elif x == y:
        return 0
    else:
        return 1

class RootDir(Dir):
    def __init__(self, path):
        Dir.__init__(self, path)
        self.path = ""
        self.all_dirs = {}
        self.all_files = {}
        self.scanpath = path
        self.latest = []

    def getName(self):
        return "/"

    def addDir(self, dir):
        self.all_dirs[dir.path] = dir

    def getDir(self, path):
        return self.all_dirs[path]

    def addGlobalFile(self, file):
        self.all_files[file.path] = file

    def getFile(self, path):
        return self.all_files[path]

    def scan(self):
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

            #TODO: This should probably be done nicer.
            if ".svn" in dirs:
                dirs.remove(".svn")

            for dir in dirs:
                dir_path = os.path.join(new_root, dir)
                dir_obj = Dir(dir_path)
                parent_dir.addSubdir(dir_obj)
                self.addDir(dir_obj)

        self.latest = self.all_files.values()
        self.latest.sort(cmp=cmpLatest)

    def getLatestAdditions(self, num=5):
        return self.latest[:num]

    def search(self, needle):
        dirs = []
        files = []

        if needle == "":
            return ([], [])

        for key in self.all_dirs.keys():
            d_name = os.path.basename(key)
            if d_name.find(needle) < 0:
                continue
            dirs.append(self.all_dirs[key])

        for key in self.all_files.keys():
            f_name = os.path.basename(key)
            if f_name.find(needle) < 0:
                continue
            files.append(self.all_files[key])

        return (dirs, files)


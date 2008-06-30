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

from pylons import config

class Dir:
    def __init__(self, path):
        self.subdirs = []
        self.files = []
        self.path = path

    def addSubdir(self, dir):
        self.subdirs.append(dir)

    def getSubdirs(self):
        return self.subdirs

    def addFile(self, file):
        self.files.append(file)

    def getFiles(self):
        return self.files

    def getPath(self):
        return self.path

    def getName(self):
        return self.path


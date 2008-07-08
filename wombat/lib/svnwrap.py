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
from pylons import config

class SvnInfo:
    """Groups svn information
    Contains information as provided by 'svn info'
    """
    def __init__(self):
        """__init__() -> SvnInfo
        Set up a new SvnInfo object with empty default values.
        """
        self.path = ""
        self.url = ""
        self.root = ""
        self.uuid = ""
        self.rev = 0
        self.kind = ""
        self.schedule = ""
        self.last_change_author = ""
        self.last_change_rev = 0
        self.last_change_date = ""

    def parse(self, stringlist):
        """parse(stringlist) -> None
        Parse the output of 'svn info'
        """
        for line in stringlist:
            if line.strip() == '':
                continue
            key, data = line.split(":", 1)
            data = data.strip()
            if key == "Path":
                self.path = data
            elif key == "URL":
                self.url = data
            elif key == "Repository Root":
                self.root = data
            elif key == "Repository UUID":
                self.uuid = data
            elif key == "Revision":
                self.rev = int(data)
            elif key == "Node Kind":
                self.kind = data
            elif key == "Schedule":
                self.schedule = data
            elif key == "Last Changed Author":
                self.last_change_author = data
            elif key == "Last Changed Rev":
                self.last_change_rev = int(data)
            elif key == "Last Changed Date":
                self.last_change_date = data

    def getPath(self):
        """getPath() -> string
        Get the path the SvnInfo object is about
        """
        return self.path

    def getUrl(self):
        """getUrl() -> string
        Get the repository url the SvnInfo object is about
        """
        return self.url

    def getRoot(self):
        """getRoot() -> string
        Get the repository's root url
        """
        return self.root

    def getUuid(self):
        """getUuid() -> string
        Get the repository's UUID
        """
        return self.uuid

    def getRev(self):
        """getRev() -> int
        Get the repository's revision number
        """
        return self.rev

    def getKind(self):
        """getKind() -> string
        Get the kind of the node this SvnInfo is about
        """
        return self.kind

    def getSchedule(self):
        """getSchedule() -> string
        Get the SvnInfo's schedule
        """
        return self.schedule

    def getLastChangeAuthor(self):
        """getLastChangeAuthor() -> string
        Get the author of the last change
        """
        return self.last_change_author

    def getLastChangeRev(self):
        """getLastChangeRev() -> int
        Get the revision when the last change happened
        """
        return self.last_change_rev

    def getLastChangeDate(self):
        """getLastChangeDate() -> string
        Get the date of the last change
        """
        return self.last_change_date

def runSvnInfo(path):
    """runSvnInfo(path) -> [string]
    Run 'svn info' on path
    Returns a string list with the output from 'svn info'
    """
    stringlist = []
    old_cwd = os.getcwd()
    os.chdir(config['app_conf']['media_dir'])
    if path == "":
        path = "."
    path = path.replace("(", "\(").replace(")","\)")
    cli_in, cli_out = os.popen2("svn info %s 2> /dev/null" % path)
    cli_in.close()
    try:
        stringlist = cli_out.readlines()
    finally:
        cli_out.close()

    os.chdir(old_cwd)
    return stringlist

def getSvnInfo(path):
    """getSvnInfo(path) -> SvnInfo
    Get an SvnInfo object for path
    """
    stringlist = runSvnInfo(path)
    svn_info = SvnInfo()
    svn_info.parse(stringlist)
    return svn_info


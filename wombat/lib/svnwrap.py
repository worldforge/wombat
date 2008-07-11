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
from wombat.lib.node_info import NodeInfo

class Info(NodeInfo):
    """Groups svn information
    Contains information as provided by 'svn info'
    """
    def __init__(self):
        """__init__() -> SvnInfo
        Set up a new SvnInfo object with empty default values.
        """
        NodeInfo.__init__(self)
        self.log = "Sorry, log messages not available via SVN yet"

    def runSvnInfo(self, path):
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

    def load(self, path):
        """string -> None
        Parse the output of 'svn info'
        """
        stringlist = self.runSvnInfo(path)

        for line in stringlist:
            if line.strip() == '':
                continue
            key, data = line.split(":", 1)
            data = data.strip()
            if key == "Last Changed Author":
                self.author = data
            elif key == "Last Changed Rev":
                self.revision = data
            elif key == "Last Changed Date":
                self.date = data


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
import md5
from pylons import config
from wombat.lib.node_info import NodeInfo

class Info(NodeInfo):
    """Load revision info from a rev file
    This class will check the meta_dir from the configuration for a file with
    the name of md5(path)_rev.md5 and parse that.
    """
    def __init__(self):
        NodeInfo.__init__(self)
        self.log = "Getting the last log message from svn doesn't work yet."

    def load(self, path):
        """string -> None
        Load metadata from files.
        """
        md5sum = md5.new(path).hexdigest()
        meta_dir = config['app_conf']['meta_dir']
        stringlist = []
        file = os.path.join(meta_dir, "%s.rev" %md5sum)
        if os.path.exists(file):
            f = open(file, 'r')
            try:
                stringlist = f.readlines()
            finally:
                f.close()
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
                elif key == "Log":
                    self.log = data
        else:
            self.author = "None loaded"
            self.revision = "None loaded"
            self.date = "None loaded"
            self.log = "File '%s' missing" % file

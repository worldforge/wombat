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

class NodeInfo:
    """Stores information about a node
    Information stored is the last person who changed the node, the revision
    identifier when the node was last changed, the date the node was last
    changed and the log message associated with the change.
    """
    def __init__(self):
        """None -> NodeInfo
        Initialize a NodeInfo object.
        """
        self.author = ""
        self.creator = ""
        self.revision = ""
        self.global_rev = ""
        self.date = ""
        self.creation_date = ""
        self.log = ""

    def load(self, path):
        """string -> None
        Load the node info from the backend
        """
        raise Exception("Implement me!")

    def getAuthor(self):
        """None -> string
        Get the author this node was last changed by
        """
        return self.author

    def getRevision(self):
        """None -> string
        Get the revision this node was last changed at
        """
        return self.revision

    def getDate(self):
        """None -> string
        Get the date this node was last changed at
        """
        return self.date

    def getLog(self):
        """None -> string
        Get the log message for the last change of this node
        """
        return self.log


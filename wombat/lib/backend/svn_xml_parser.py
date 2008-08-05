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

from StringIO import StringIO
from xml.dom import minidom

class Svn(object):
    def __init__(self):
        self.path = u''
        self.author = u''
        self.revision = 0
        self.date = ''
        self.root = u''
        self.msg = u'No commit message.'

class SvnParser(object):
    def __init__(self):
        self.svn = Svn()

    def parse(self, node):
        parse_fun = getattr(self, "parse%s" % node.__class__.__name__)
        parse_fun(node)

    def parseChildNodes(self, node):
        for child in node.childNodes:
            self.parse(child)

    def parseComment(self, node):
        pass

    def parseDocument(self, node):
        self.parse(node.documentElement)

    def parseElement(self, node):
        handler_fun = getattr(self, "do_%s" % node.tagName.replace('-','_'), self.do_nyi)
        handler_fun(node)

    def parseText(self, node):
        pass

    def do_nyi(self, node):
        print "Parsing tag <%s> is not implemented." % node.tagName

    def do_entry(self, node):
        self.svn.path = node.attributes['path'].value
        self.parseChildNodes(node)

    def do_url(self, node):
        """Ignore <url> tags"""
        pass

    def do_repository(self, node):
        self.parseChildNodes(node)

    def do_uuid(self, node):
        """Ignore <uuid> tags"""
        pass

    def do_root(self, node):
        self.svn.root = node.childNodes[0].nodeValue

    def do_wc_info(self, node):
        """Ignore <wc-info> tags and children."""
        pass

    def do_commit(self,node):
        self.svn.revision = int(node.attributes['revision'].value)
        self.parseChildNodes(node)

    def do_author(self, node):
        self.svn.author = node.childNodes[0].nodeValue

    def do_date(self, node):
        date_str = node.childNodes[0].nodeValue
        date_date = date_str[:date_str.index('T')]
        date_time = date_str[date_str.index('T')+1:date_str.index('.')]
        self.svn.date = u"%s %s" % (date_date, date_time)

    def do_logentry(self, node):
        self.svn.revision = int(node.attributes['revision'].value)
        self.parseChildNodes(node)

    def do_msg(self, node):
        self.svn.msg = node.childNodes[0].nodeValue.strip()

def parse_svn(xml_text):
    xml_stream = StringIO(xml_text)
    xmldom = minidom.parse(xml_stream)
    xml_stream.close()

    p = SvnParser()
    p.parse(xmldom)
    return p.svn


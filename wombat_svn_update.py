#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import getopt
import sys

VERSION="0.1.3"
debug = False

def usage(name):
    """Print usage information
    """
    print """Usage: %s [options] <media repo> <metadata dir>
Possible options are:
--help        -h       Display this help text.
--debug       -d       Print debugging output.
--version     -V       Print the version.
""" % name

def update(media_dir):
    """string -> None
    Update the svn repo
    """
    cwd = os.getcwd()
    os.chdir(media_dir)
    os.system("svn update")
    os.chdir(cwd)

def clear_meta_dir(meta_dir):
    """string -> None
    Remove *.rev files
    FIXME: Deleting the files could be done better.
    """
    if debug:
        print "Clearing meta_dir"

    cwd = os.getcwd()
    os.chdir(meta_dir)
    os.system("rm -r *.rev")
    os.chdir(cwd)

def create_rev_file(path, meta_dir):
    """string, string -> None
    Actually generate the meta_dir/md5sum(path).rev file
    """
    if debug:
        print "Generating rev data for %s" % path

    path_hash = md5.new(path)
    rev_file_name = "%s.rev" % path_hash.hexdigest()
    rev_file_path = os.path.join(meta_dir, rev_file_name)
    if not os.path.exists(meta_dir):
        os.mkdir(meta_dir)
    f = open(rev_file_path, 'w')

    stringlist = []
    if path == "":
        path = "."
    cli_in, cli_out = os.popen2("svn info '%s' 2> /dev/null" % path)
    cli_in.close()
    try:
        stringlist = cli_out.readlines()
    finally:
        cli_out.close()

    try:
        f.writelines(stringlist)
    finally:
        f.close()

def generate_rev_data(media_dir, meta_dir):
    """string, string -> None
    Iterate over the media dir and generate md5sum(path).rev files
    """
    cwd = os.getcwd()
    os.chdir(media_dir)
    for root, dirs, files in os.walk(media_dir):
        new_root = root.replace(media_dir,'').lstrip('/')
        create_rev_file(new_root, meta_dir)
        for file in files:
            file_path = os.path.join(new_root, file)
            create_rev_file(file_path, meta_dir)

        if ".svn" in dirs:
            dirs.remove(".svn")

def main(argv):
    global debug
    try:
        opts, args = getopt.getopt(argv[1:], "hdV",
            ["help","debug","version"])
    except getopt.GetoptError:
        usage(argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-V", "--version"):
            print "%s %s" % (argv[0], VERSION)
            sys.exit(0)

    if len(args) < 2:
        usage(argv[0])
        sys.exit(23)

    media_dir = os.path.abspath(args[0])
    meta_dir = os.path.abspath(args[1])

    if debug:
        print "Media repository: %s" % media_dir
        print "Metadata directory: %s" % meta_dir

    update(media_dir)
    clear_meta_dir(meta_dir)
    generate_rev_data(media_dir, meta_dir)


if __name__ == "__main__":
    main(sys.argv)

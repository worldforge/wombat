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

import md5
import random

VALID_CHARS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#^&"

def random_salt():
    """None -> string
    Generate a random 8-character salt string
    """
    salt = u"".join(random.sample(VALID_CHARS, 8))
    return salt

def random_token():
    """None -> string
    Generate a random 16byte token.
    """
    token = unicode(hex(random.getrandbits(16*8))).lstrip('0x').rstrip('L')
    return token

def crypt_password(password):
    """string -> string
    Generate an encrypted password.
    """
    salt = random_salt()
    md5_hash = md5.md5(salt)
    md5_hash.update(unicode(password))
    crypt_pass = unicode(md5_hash.hexdigest())
    return u"{MD5}$%s$%s" % (salt, crypt_pass)

def parse_pass(pass_string):
    """string -> (string, string, string)
    Parse an encrypted password.
    """
    return tuple(pass_string.split("$"))

def check_password(stored, provided):
    """string, string -> boolean
    Check if the encrypted stored password matches the provided plaintext
    password.
    """
    method, salt, crypt_pass = parse_pass(stored)
    # Here we could check the method if we at some point decide to use more than
    # just md5

    # Check that the stored password parsed correctly
    if salt is None or crypt_pass is None:
        return False

    md5_hash = md5.md5(salt)
    md5_hash.update(unicode(provided))

    return crypt_pass == unicode(md5_hash.hexdigest())


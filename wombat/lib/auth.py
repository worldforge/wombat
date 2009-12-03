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

import hashlib
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

def crypt_password_md5(password):
    """string -> string
    Generate an MD5 encrypted password.
    """
    salt = random_salt()
    md5_hash = hashlib.md5(salt)
    md5_hash.update(unicode(password))
    crypt_pass = unicode(md5_hash.hexdigest())
    return u"{MD5}$%s$%s" % (salt, crypt_pass)

def crypt_password_md5k(password):
    salt = random_salt()
    md5_hash = hashlib.md5(salt)
    md5_hash.update(unicode(password))
    for i in range(10000):
        md5_hash.update(md5_hash.hexdigest())
    crypt_pass = unicode(md5_hash.hexdigest())
    return u"{MD5k}$%s$%s" % (salt, crypt_pass)

password_methods = {
        "MD5" : crypt_password_md5,
        "MD5k" : crypt_password_md5k }

def crypt_password(password, method="MD5k"):
    """string, string -> string
    Generate an encrypted password using the method specified.
    """
    function = password_methods[method]
    return function(password)

def parse_pass(pass_string):
    """string -> (string, string, string)
    Parse an encrypted password.
    """
    return tuple(pass_string.split("$"))

def check_password_md5(crypt_pass, salt, provided):
    """string, string -> boolean
    Check if the encrypted stored md5 password matches the provided plaintext
    password.
    """
    md5_hash = hashlib.md5(salt)
    md5_hash.update(unicode(provided))

    return crypt_pass == unicode(md5_hash.hexdigest())

def check_password_md5k(crypt_pass, salt, provided):
    """string, string -> boolean
    Check if the encrypted stored md5k password matches the provided plaintext
    password.
    """
    md5_hash = hashlib.md5(salt)
    md5_hash.update(unicode(provided))
    for i in range(10000):
        md5_hash.update(md5_hash.hexdigest())

    return crypt_pass == unicode(md5_hash.hexdigest())

check_methods = {
        "{MD5}" : check_password_md5,
        "{MD5k}" : check_password_md5k }

def check_password(stored, provided):
    """string, string -> boolean
    Check if the encrypted stored password matches the provided plaintext
    password.
    """
    method, salt, crypt_pass = parse_pass(stored)

    # Check that the stored password parsed correctly
    if method is None or salt is None or crypt_pass is None:
        return False

    try:
        function = check_methods[method]
        return function(crypt_pass, salt, provided)
    except KeyError:
        return False



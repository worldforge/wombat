# Copyright (C) 2009 by Kai Blin
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

from wombat.lib.auth import crypt_password, parse_pass, check_password
import hashlib

def test_parse_pass():
    password = u"{method}$SALTSALT$PASSWORDPASSWORD"
    method, salt, crypt = parse_pass(password)
    assert method == "{method}", "failed to parse method"
    assert salt == "SALTSALT", "failed to parse salt"
    assert crypt == "PASSWORDPASSWORD"

def test_password_MD5():
    pass_string = crypt_password("secret", "MD5")
    method, salt, crypt = parse_pass(pass_string)
    assert method == "{MD5}", "method is %s, not {MD5}" % method
    assert salt is not None, "salt is None"

    md5_hash = hashlib.md5(salt)
    md5_hash.update(u"secret")

    assert crypt == md5_hash.hexdigest(), "Crypted password did not match"

def test_check_password_MD5():
    pass_string = crypt_password("secret", "MD5")
    assert check_password(pass_string, "secret"), "Password verification failed"

    pass_string = crypt_password("geheim", "MD5")
    assert check_password(pass_string, "secret") == False, "Password verification passed for wrong password"

def test_password_MD5k():
    pass_string = crypt_password("secret", "MD5k")
    method, salt, crypt = parse_pass(pass_string)
    assert method == "{MD5k}", "method is %s, not {MD5k}" % method
    assert salt is not None, "salt is None"

    md5_hash = hashlib.md5(salt)
    md5_hash.update(u"secret")
    for i in range(10000):
        md5_hash.update(md5_hash.hexdigest())

    assert crypt == md5_hash.hexdigest(), "Crypted password did not match"

def test_check_password_MD5k():
    pass_string = crypt_password("secret", "MD5k")
    assert check_password(pass_string, "secret"), "Password verification failed"

    pass_string = crypt_password("geheim", "MD5k")
    assert check_password(pass_string, "secret") == False, "Password verification passed for wrong password"



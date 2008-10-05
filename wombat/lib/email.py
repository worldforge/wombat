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

import smtplib
import datetime
from wombat.lib.base import config
import wombat.lib.helpers as h

def send_mail(toaddr, msg):
    """(string, string) -> None
    Send an email to <toaddr>
    """
    server = smtplib.SMTP(config['app_conf']['smtpserver'])
    fromaddr = config['app_conf']['email_from']

    #TODO: Catch errors here once I decided how to handle those error cases.
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

def create_password_reset_msg(toaddr, token):
    """(string, string) -> string
    Create the email headers/body of a password reset email.
    """
    d = {
            "from": config['app_conf']['email_from'],
            "to": toaddr,
            "date":  datetime.datetime.now().ctime(),
            "appname": config['app_conf']['site_name'],
            "reset_url": h.url_for(controller='account', action='reset',
                id=token, qualified=True),
            "cancel_url": h.url_for(controller='account', action='cancel_reset',
                id=token, qualified=True)
        }

    msg = """From: %(from)s
To: %(to)s
Date: %(date)s
Subject: [%(appname)s] password reset.

Somebody, probably you, requested a password reset for your %(appname)s account
%(to)s.

To reset your password, go to %(reset_url)s .

To cancel the request, please go to %(cancel_url)s .
""" % d
    msg = msg.replace('\n', '\r\n')

    return msg



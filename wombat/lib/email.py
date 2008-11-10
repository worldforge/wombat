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

class EmailException(Exception):
    pass

def send_mail(toaddr, msg):
    """(string, string) -> None
    Send an email to <toaddr>
    """
    servername = config['app_conf']['smtpserver']

    # skip fake server name used for tests.
    if servername == "fake.example.com":
        return

    server = smtplib.SMTP(servername)
    fromaddr = config['app_conf']['email_from']

    try:
        server.sendmail(fromaddr, toaddr, msg)
    except smtplib.SMTPRecipientsRefused:
        raise EmailException("Recipients refused.")
    except:
        raise EmailException("Unknown error sending email.")
    finally:
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

def create_account_activation_msg(toaddr, token):
    """(string, string) -> string
    Create the email headers/body of an account activation email.
    """
    d = {
            "from": config['app_conf']['email_from'],
            "to": toaddr,
            "date":  datetime.datetime.now().ctime(),
            "appname": config['app_conf']['site_name'],
            "activate_url": h.url_for(controller='account', action='activate',
                id=token, qualified=True),
            "cancel_url": h.url_for(controller='account', action='cancel_account',
                id=token, qualified=True)
        }

    msg = """From: %(from)s
To: %(to)s
Date: %(date)s
Subject: [%(appname)s] account activation.

Somebody, probably you, created a %(appname)s account for your address
%(to)s.

To activate your account, go to %(activate_url)s .

To cancel the account, please go to %(cancel_url)s .
""" % d
    msg = msg.replace('\n', '\r\n')

    return msg


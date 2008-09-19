import logging

import md5
from wombat.lib.base import *
from wombat.model import User, UserData

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def login(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Login user'
        c.messages = []
        c.session = Session()

        if 'user' in session:
            redirect_to(action='logged_in')

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        return render('/derived/auth/login.html')

    def submit(self, id):
        form_email = str(request.params.get('email'))
        form_password = str(request.params.get('password'))

        s = Session()
        user = s.query(User).filter_by(email=unicode(form_email)).first()
        if user is None:
            if id == "ajax":
                return "no such user"
            session['messages'] = ["No such user"]
            session.save()

            redirect_to(action='login')

        if user.password != md5.md5(form_password).hexdigest():
            if id == "ajax":
                return "password mismatch"
            session['messages'] = ["Password mismatch"]
            session.save()

            redirect_to(action='login')

        session['user'] = user
        session.save()

        if id == "ajax":
            return "success"
        else:
            if session.get('path_before_login'):
                redirect_to(session.get('path_before_login'))
            else:
                redirect_to(action='logged_in')

    def check(self):
        if 'user' in session:
            return "Logged in as %s" % session['user'].email
        else:
            return "Not logged in"

    def logged_in(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Logged in'
        c.messages = []
        c.session = Session()

        c.user = session.get('user')
        if c.user is None:
            redirect_to(action='login')

        return render('/derived/auth/logged_in.html')

    def logout(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Logged out'
        c.messages = []
        c.session = Session()

        if 'user' in session:
            del session['user']
            session.save()

        if id == "ajax":
            return "logged out"

        return render('/derived/auth/logout.html')


import logging

import md5
from wombat.lib.base import *
from wombat.model import User

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def login(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Login user'
        c.messages = []
        c.session = Session()

        if 'user' in session:
            redirect_to(action='logged_in')

        return render('/derived/login/login.html')

    def submit(self, id):
        form_email = str(request.params.get('email'))
        form_password = str(request.params.get('password'))

        s = Session()
        user = s.query(User).get_by(email=unicode(form_email))
        if user is None:
            if id == "ajax":
                return "no such user"
            redirect_to(action='login')

        if user.password != md5.md5(form_password).hexdigest():
            if id == "ajax":
                return "password mismatch"
            redirect_to(action='login')

        session['user'] = form_email
        session.save()

        if id == "ajax":
            return "success"
        else:
            if session.get('path_before_login'):
                redirect_to(session.get('path_before_login'))
            else:
                redirect_to(action='logged_in')

    def check(self, id):
        if id is None:
            if 'user' in session:
                return "Logged in as %s" % session['user']
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

        return render('/derived/login/logged_in.html')

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

        return render('/derived/login/logout.html')


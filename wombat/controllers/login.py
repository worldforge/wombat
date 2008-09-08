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

    def submit(self):
        form_email = str(request.params.get('email'))
        form_password = str(request.params.get('password'))

        s = Session()
        user = s.query(User).get_by(email=unicode(form_email))
        if user is None:
            redirect_to(action='login')

        if user.password != md5.md5(form_password).hexdigest():
            redirect_to(action='login')

        session['user'] = form_email
        session.save()

        if session.get('path_before_login'):
            redirect_to(session.get('path_before_login'))
        else:
            redirect_to(action='logged_in')

    def logged_in(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Logged in'
        c.messages = []
        c.session = Session()

        c.user = session.get('user')
        if c.user is None:
            redirect_to(action='login')

        return render('/derived/login/logged_in.html')

    def logout(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Logged out'
        c.messages = []
        c.session = Session()

        if 'user' in session:
            del session['user']
            session.save()

        return render('/derived/login/logout.html')


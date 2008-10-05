import logging

import md5
from wombat.lib.base import *
from wombat.lib.auth import check_password
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
                return "password mismatch"
            session['messages'] = ["Password mismatch"]
            session.save()

            redirect_to(action='login')

        if not user.active:
            if id == "ajax":
                return "account disabled"
            session['messages'] = ["Account disabled"]
            session.save()

            redirect_to(action='login')

        if not check_password(user.password, form_password):
            if id == "ajax":
                return "password mismatch"
            session['messages'] = ["Password mismatch"]
            session.save()

            redirect_to(action='login')

        session['user'] = user.id
        session.save()

        if id == "ajax":
            return "success"
        else:
            path_info = session.get('path_before_login')
            if path_info is not None:
                del session['path_before_login']
                session.save()
                redirect_to(path_info)
            else:
                redirect_to(action='logged_in')

    def check(self):
        if 'user' in session:
            s = Session()
            db_user = s.query(User).get(session['user'])
            if db_user:
                return "Logged in as %s" % db_user.email
            else:
                return "Database error"
        else:
            return "Not logged in"

    def logged_in(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Logged in'
        c.messages = []
        c.session = Session()

        user_id = session.get('user')
        if user_id is None:
            redirect_to(action='login')

        c.user = c.session.query(User).get(user_id)
        if c.user is None:
            del session['user']
            session.save()
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


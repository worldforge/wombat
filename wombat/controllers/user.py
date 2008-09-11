import logging

import md5
from wombat.lib.base import *
from wombat.model import User, UserData

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def login(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Login user'
        c.messages = []
        c.session = Session()

        if 'user' in session:
            redirect_to(action='logged_in')

        return render('/derived/user/login.html')

    def submit(self, id):
        form_email = str(request.params.get('email'))
        form_password = str(request.params.get('password'))

        s = Session()
        user = s.query(User).filter_by(email=unicode(form_email)).first()
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

        return render('/derived/user/logged_in.html')

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

        return render('/derived/user/logout.html')

    def register(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Register new user'
        c.messages = []
        c.session = Session()

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        return render('/derived/user/register.html')

    def _is_email_valid(self, email):
        # does it contain exactly one '@'?
        if email.count('@') != 1:
            return False

        # TODO: Add more email validity tests
        return True

    def signup(self, id):
        user_email = unicode(request.params.get('user_email'))
        user_email_c = unicode(request.params.get('user_email_confirm'))

        s = Session()

        if user_email != user_email_c:
            if id == "ajax":
                return "email address mismatch"
            else:
                session['messages'] = ["Email address mismatch"]
                session.save()
                redirect_to(action="register")

        if not self._is_email_valid(user_email):
            if id == "ajax":
                return "invalid email address"
            else:
                session['messages'] = ["Invalid email address"]
                session.save()
                redirect_to(action="register")

        if s.query(User).filter_by(email=user_email).first() is not None:
            if id == "ajax":
                return "email already associated with an account"
            else:
                session['messages'] = ["Email already associated with an account"]
                session.save()
                redirect_to(action="register")

        user_pass = unicode(request.params.get('user_pass'))
        user_pass_c = unicode(request.params.get('user_pass_confirm'))

        if user_pass != user_pass_c:
            if id == "ajax":
                return "password mismatch"
            else:
                session['messages'] = ["Password mismatch"]
                session.save()
                redirect_to(action="register")

        if request.params.get('user_vcs_pass') is not None:
            vcs_pass = unicode(request.params.get('user_vcs_pass'))
            vcs_pass_c = unicode(request.params.get('user_vcs_pass_confirm'))

            if vcs_pass != vcs_pass_c:
                if id == "ajax":
                    return "VCS password mismatch"
                else:
                    session['messages'] = ["VCS password mismatch"]
                    session.save()
                    redirect_to(action="register")
        else:
            vcs_pass = None

        if request.params.get('user_name') is not None:
            user_name = unicode(request.params.get('user_name'))
        else:
            user_name = u"Unnamed User"

        if request.params.get('user_nick') is not None:
            user_nick = unicode(request.params.get('user_nick'))
        else:
            user_nick = u"Anonymous"

        if request.params.get('user_vcs_user') is not None:
            vcs_user = unicode(request.params.get('user_vcs_user'))
        else:
            vcs_user = None

        user = User(user_email, md5.md5(user_pass).hexdigest())
        data = UserData(user_name, user_nick, vcs_user, vcs_pass)
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        # TODO: Look into sending a registration confirmation email.
        if id == "ajax":
            return "user successfully registered"
        else:
            redirect_to(action="registered")

    def registered(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Registered'
        c.messages = []
        c.session = Session()

        return render('/derived/user/registered.html')


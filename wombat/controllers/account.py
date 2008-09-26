import logging

import md5
from wombat.lib.base import *
from wombat.model import User, UserData

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def register(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Register new user'
        c.messages = []
        c.session = Session()

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        return render('/derived/account/register.html')

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

        user = User(user_email, unicode(md5.md5(user_pass).hexdigest()))
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

        return render('/derived/account/registered.html')

    def index(self):
        c.title = 'Account Index'
        c.messages = []
        c.session = Session()
        c.accounts = c.session.query(User).all()

        return render('/derived/account/index.html')

    def edit(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Edit Account'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        c.account = c.session.query(User).get(id)
        if c.account is None:
            abort(404)

        if not 'user' in session:
            abort(403)

        #TODO: Admin users should be able to edit accounts as well.
        if session['user'] != c.account.id:
            abort(403)

        return render('/derived/account/edit.html')

    def change(self, id):
        user_email = unicode(request.params.get('user_email'))
        user_email_c = unicode(request.params.get('user_email_confirm'))

        if not 'user' in session:
            abort(403)

        s = Session()
        user = s.query(User).get(session['user'])
        if user is None:
            abort(404)

        if user_email != user_email_c:
            if id == "ajax":
                return "email address mismatch"
            else:
                session['messages'] = ["Email address mismatch"]
                session.save()
                redirect_to(action="edit")

        if not self._is_email_valid(user_email):
            if id == "ajax":
                return "invalid email address"
            else:
                session['messages'] = ["Invalid email address"]
                session.save()
                redirect_to(action="edit")

        # check if the email matches the current user's email
        u_by_email = s.query(User).filter_by(email=user_email).first()

        if u_by_email is not None:
            if u_by_email.id != user.id:
                if id == "ajax":
                    return "email already associated with an account"
                else:
                    session['messages'] = ["Email already associated with an account"]
                    session.save()
                    redirect_to(action="edit")

        user.email = user_email

        user_pass = unicode(request.params.get('user_pass'))
        user_pass_c = unicode(request.params.get('user_pass_confirm'))

        if user_pass != user_pass_c:
            if id == "ajax":
                return "password mismatch"
            else:
                session['messages'] = ["Password mismatch"]
                session.save()
                redirect_to(action="edit")

        if user_pass != "":
            user.password = unicode(md5.md5(user_pass).hexdigest())

        if request.params.get('user_vcs_pass') is not None:
            vcs_pass = unicode(request.params.get('user_vcs_pass'))
            vcs_pass_c = unicode(request.params.get('user_vcs_pass_confirm'))

            if vcs_pass != vcs_pass_c:
                if id == "ajax":
                    return "VCS password mismatch"
                else:
                    session['messages'] = ["VCS password mismatch"]
                    session.save()
                    redirect_to(action="edit")

                user.user_data.vcs_pass = vcs_pass

        if request.params.get('user_name') is not None:
            user_name = unicode(request.params.get('user_name'))
        else:
            user_name = u"Unnamed User"

        user.user_data.name = user_name

        if request.params.get('user_nick') is not None:
            user_nick = unicode(request.params.get('user_nick'))
        else:
            user_nick = u"anonymous"

        user.user_data.nick = user_nick

        if request.params.get('user_vcs_user') is not None:
            vcs_user = unicode(request.params.get('user_vcs_user'))
            user.user_data.vcs_user = vcs_user
        else:
            vcs_user = None

        s.update(user)
        s.commit()

        if id == "ajax":
            return "user data updated"
        else:
            redirect_to(action='changed', id=None)

    def changed(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Updated Account'
        c.messages = []
        c.session = Session()

        return render('derived/account/changed.html')

    def enable(self, id):
        if id is None:
            abort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            abort(404)

        #TODO: check for admin role
        user.active = True
        s.update(user)
        s.commit()

        return "account %s enabled" % user.email

    def disable(self, id):
        if id is None:
            avort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            abort(404)

        #TODO: check for admin role
        user.active = False
        s.update(user)
        s.commit()

        return "account %s disabled" % user.email

    def delete(self, id):
        if id is None:
            abort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            return (404)

        if not 'user' in session:
            abort(403)

        #TODO: Check for admin permissions heere
        if session['user'] == user.id:
            s.delete(user.user_data)
            s.delete(user)
            s.commit()

            return "Your account has been deleted."
        else:
            return "Failed to delete account"


import logging

import md5
from wombat.lib.base import *
from wombat.lib.auth import crypt_password, random_token
from wombat.lib.email import *
from wombat.lib.roles import require_roles, require_login
from wombat.model import User, UserData, ResetData, EmailConfirm

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

    def signup(self, id=None):
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

        user = User(user_email, crypt_password(user_pass))
        data = UserData(user_name, user_nick, vcs_user, vcs_pass)
        data.user = user
        s.add(user)
        s.add(data)

        token = random_token()
        msg = create_account_activation_msg(user.email, token)

        act_data = EmailConfirm(token, user.email)
        s.add(act_data)
        s.commit()

        try:
            send_mail(user.email, msg)
        except EmailException, e:
            if id == "ajax":
                return "sending account registration failed: %s" % e.message
            session['email_error'] = e.message
            session.save()

        if id == "ajax":
            return "user successfully registered"
        else:
            redirect_to(action="registered")

    def registered(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Registered'
        c.messages = []
        c.session = Session()

        if 'email_error' in session:
            c.email_error = session['email_error']
            del session['email_error']
            session.save()

        return render('/derived/account/registered.html')

    def activate(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Account activated.'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        act_data = c.session.query(EmailConfirm).filter_by(token=unicode(id)).first()

        if act_data is None:
            abort(404)

        user = c.session.query(User).filter_by(email=act_data.email).first()
        if user is None:
            c.session.delete(act_data)
            c.session.commit()
            abort(404)

        user.active = True
        c.session.add(user)
        c.session.delete(act_data)
        c.session.commit()

        return render('/derived/account/activate.html')

    def cancel_account(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Account cancelled'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        act_data = c.session.query(EmailConfirm).filter_by(token=unicode(id)).first()

        if act_data is None:
            abort(404)

        user = c.session.query(User).filter_by(email=act_data.email).first()
        if user is not None:
            # Can't cancel accounts that were already activated.
            if user.active:
                abort(403)

            c.session.delete(user.user_data)
            c.session.delete(user)

        c.session.delete(act_data)
        c.session.commit()

        return render('/derived/account/cancel_account.html')

    @require_login
    def index(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Account Index'
        c.messages = []
        c.session = Session()
        accounts = c.session.query(User)

        needle = unicode(request.params.get('q'))

        #conversion to unicode gives us a 'None' string instead of None.
        if needle != u'None':
            from sqlalchemy import or_
            accounts = accounts.filter(User.id == UserData.user_id).filter(
                    or_(User.email.like(u"%%%s%%" % needle),
                    or_(UserData.name.like(u"%%%s%%" % needle),
                    or_(UserData.nick.like(u"%%%s%%" % needle),
                        UserData.vcs_user.like(u"%%%s%%" % needle)))))

        c.accounts = accounts.all()
        return render('/derived/account/index.html')

    @require_roles(['owner', 'admin'])
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

        session['edit_user'] = c.account.id
        session.save()

        return render('/derived/account/edit.html')

    @require_roles(['owner', 'admin'])
    def change(self, id=None):
        user_email = unicode(request.params.get('user_email'))
        user_email_c = unicode(request.params.get('user_email_confirm'))

        edit_user = session.get('edit_user')
        if edit_user is None:
            abort(404)

        del session['edit_user']
        session.save()

        s = Session()
        user = s.query(User).get(edit_user)
        if user is None:
            abort(404)

        if user_email != user_email_c:
            if id == "ajax":
                return "email address mismatch"
            else:
                session['messages'] = ["Email address mismatch"]
                session.save()
                redirect_to(action="edit", id=edit_user)

        if not self._is_email_valid(user_email):
            if id == "ajax":
                return "invalid email address"
            else:
                session['messages'] = ["Invalid email address"]
                session.save()
                redirect_to(action="edit", id=edit_user)

        # check if the email matches the current user's email
        u_by_email = s.query(User).filter_by(email=user_email).first()

        if u_by_email is not None:
            if u_by_email.id != user.id:
                if id == "ajax":
                    return "email already associated with an account"
                else:
                    session['messages'] = ["Email already associated with an account"]
                    session.save()
                    redirect_to(action="edit",id=edit_user)

        user.email = user_email

        user_pass = unicode(request.params.get('user_pass'))
        user_pass_c = unicode(request.params.get('user_pass_confirm'))

        if user_pass != user_pass_c:
            if id == "ajax":
                return "password mismatch"
            else:
                session['messages'] = ["Password mismatch"]
                session.save()
                redirect_to(action="edit", id=edit_user)

        if user_pass != "":
            user.password = crypt_password(user_pass)

        if request.params.get('user_vcs_pass') is not None:
            vcs_pass = unicode(request.params.get('user_vcs_pass'))
            vcs_pass_c = unicode(request.params.get('user_vcs_pass_confirm'))

            if vcs_pass != vcs_pass_c:
                if id == "ajax":
                    return "VCS password mismatch"
                else:
                    session['messages'] = ["VCS password mismatch"]
                    session.save()
                    redirect_to(action="edit", id=edit_user)

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

        s.add(user)
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

    @require_roles(['admin'])
    def enable(self, id):
        if id is None:
            abort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            abort(404)

        user.active = True
        s.add(user)
        s.commit()

        return "account %s enabled" % user.email

    @require_roles(['admin'])
    def disable(self, id):
        if id is None:
            avort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            abort(404)

        user.active = False
        s.add(user)
        s.commit()

        return "account %s disabled" % user.email

    @require_roles(['owner', 'admin'])
    def delete(self, id):
        if id is None:
            abort(404)

        s = Session()
        user = s.query(User).get(id)

        if user is None:
            return (404)

        s.delete(user.user_data)
        s.delete(user)
        s.commit()

        return "Your account has been deleted."

    def request_reset(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Request account reset.'
        c.messages = []
        c.session = Session()

        return render('/derived/account/request_reset.html')

    def handle_reset_request(self, id=None):
        s = Session()
        toaddr = request.params.get('email_addr')

        if not self._is_email_valid(toaddr):
            if id == "ajax":
                return "invalid email address"
            session['messages'] = ['Invalid email address']
            session.save()
            redirect_to(action='request_reset')

        user = s.query(User).filter_by(email=unicode(toaddr)).first()

        # We always claim we sent an email to stop people from farming our
        # database for email addresses of users.
        if user is None:
            if id == "ajax":
                return "sent password reset email"
            redirect_to(action="reset_request_sent")

        token = random_token()

        msg = create_password_reset_msg(toaddr, token)
        reset_data = ResetData(token, toaddr)
        s.save(reset_data)
        s.commit()

        try:
            send_mail(toaddr, msg)
        except EmailException, e:
            if id == "ajax":
                return "Sending password reset email failed: %s" % e.message
            session['email_error'] = e.message
            session.save()

        if id == "ajax":
            return "sent password reset email"
        redirect_to(action='request_reset_sent')

    def request_reset_sent(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Password reset sent'
        c.messages = []
        c.session = Session()

        if "email_error" in session:
            c.email_error = session["email_error"]
            del session["email_error"]
            session.save()

        return render('/derived/account/request_reset_sent.html')

    def reset(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Password reset cancelled'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        c.id = id
        c.reset_data = c.session.query(ResetData).filter_by(token=unicode(id)).first()

        if c.reset_data is None:
            abort(404)

        if 'messages' in session:
            c.messages += session['messages']
            del session['messages']
            session.save()

        return render('/derived/account/reset.html')

    def handle_reset(self, id):
        if id is None:
            abort(404)

        s = Session()
        reset_data = s.query(ResetData).filter_by(token=unicode(id)).first()

        if reset_data is None:
            abort(404)

        # Just a small sanity check if the user was deleted between creating the
        # reset request and resetting the password
        user = s.query(User).filter_by(email=reset_data.email).first()
        if user is None:
            s.delete(reset_data)
            s.commmit()
            abort(404)

        password = unicode(request.params.get('new_password'))
        password_conf = unicode(request.params.get('new_password_conf'))

        if password != password_conf:
            session['messages'] = ["Password mismatch"]
            session.save()
            redirect_to(action='reset', id=reset_data.token)

        user.password = crypt_password(password)
        s.add(user)
        s.delete(reset_data)
        s.commit()

        redirect_to(action='reset_complete', id=None)

    def reset_complete(self):
        c.name = config['app_conf']['site_name']
        c.title = 'Password reset complete'
        c.messages = []
        c.session = Session()

        return render('/derived/account/reset_complete.html')

    def cancel_reset(self, id):
        c.name = config['app_conf']['site_name']
        c.title = 'Password reset cancelled'
        c.messages = []
        c.session = Session()

        if id is None:
            abort(404)

        reset_data = c.session.query(ResetData).filter_by(token=unicode(id)).first()

        if reset_data is None:
            abort(404)

        c.session.delete(reset_data)
        c.session.commit()

        return render('/derived/account/cancel_reset.html')


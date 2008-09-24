import md5
from wombat.tests import *

class TestAccountController(TestController):

    def test_register(self):
        res = self.app.get(url_for(controller='account', action='register'))

        form = None
        for key in res.forms.keys():
            if 'user_email' in res.forms[key].fields:
                form = res.forms[key]

        self.assertNotEqual(form, None)

        new_res = form.submit()
        res = new_res.follow()
        res.mustcontain("Invalid email address")

        # 'test' should be an invalid email address
        form['user_email'] = "test"
        form['user_email_confirm'] = "test"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Invalid email address")

        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "testus@localhost"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Email address mismatch")

        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@localhost"
        form['user_pass'] = "test"
        form['user_pass_confirm'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Password mismatch")

        # now fill out the full form, just get the vcs password wrong this time
        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@localhost"
        form['user_pass'] = "secret"
        form['user_pass_confirm'] = "secret"
        form['user_name'] = "Test Tester"
        form['user_nick'] = "test"
        form['user_vcs_user'] = "test"
        form['user_vcs_pass'] = "test"
        form['user_vcs_pass_confirm'] = "taste"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("VCS password mismatch")

        # finally do everything right
        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@localhost"
        form['user_pass'] = "secret"
        form['user_pass_confirm'] = "secret"
        form['user_name'] = "Test Tester"
        form['user_nick'] = "test"
        form['user_vcs_user'] = "test"
        form['user_vcs_pass'] = "test"
        form['user_vcs_pass_confirm'] = "test"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("account registration has been received")

        s = model.Session()
        user = s.query(model.User).filter_by(email=u"test@localhost").first()

        self.assertEqual(user.user_data.name, u"Test Tester")
        self.assertEqual(user.user_data.nick, u"test")
        self.assertEqual(user.user_data.vcs_user, u"test")
        self.assertEqual(user.user_data.vcs_pass, u"test")

        # and now try to register the same user, should fail
        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@localhost"
        form['user_pass'] = "secret"
        form['user_pass_confirm'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Email already associated with an account")

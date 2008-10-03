from wombat.tests import *
from wombat.lib.auth import crypt_password

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

        self.assertTrue(user is not None)
        self.assertEqual(user.user_data.name, u"Test Tester")
        self.assertEqual(user.user_data.nick, u"test")
        self.assertEqual(user.user_data.vcs_user, u"test")
        self.assertEqual(user.user_data.vcs_pass, u"test")
        self.assertFalse(user.active)

        # and now try to register the same user, should fail
        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@localhost"
        form['user_pass'] = "secret"
        form['user_pass_confirm'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Email already associated with an account")

    def test_index(self):
        res = self.app.get(url_for(controller='account'))

        self.assertEqual(res.c.accounts, [])

        s = model.Session()
        # create a user that's already active
        user = model.User(u"test@localhost", crypt_password('secret'), True)
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        res = self.app.get(url_for(controller='account'))

        self.assertEqual(len(res.c.accounts), 1)
        acc = res.c.accounts[0]
        self.assertEqual(acc.id, user.id)

    def test_edit(self):
        res = self.app.get(url_for(controller='account', action='edit'),
                status=404)

        res = self.app.get(url_for(controller='account', action='edit', id=1),
                status=404)

        s = model.Session()
        # create a user that's already active
        user = model.User(u"test@localhost", crypt_password('secret'), True)
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        res = self.app.get(url_for(controller='account', action='edit', id=1),
                status=403)

        tmp_res = self.app.post(url_for(controller='auth', action='submit', id='ajax'),
                params={'email':'test@localhost', 'password':'secret'})
        tmp_res.mustcontain("success")


        res = self.app.get(url_for(controller='account', action='edit', id=1))

        form = None
        for key in res.forms.keys():
            if 'user_email' in res.forms[key].fields:
                form = res.forms[key]

        self.assertNotEqual(form, None)

        # check the default values are ok
        self.assertEqual(form['user_email'].value, user.email)
        self.assertEqual(form['user_email_confirm'].value, user.email)
        self.assertEqual(form['user_name'].value, data.name)
        self.assertEqual(form['user_nick'].value, data.nick)
        self.assertEqual(form['user_vcs_user'].value, data.vcs_user)

        # Now try to save changes
        # first do it wrong
        form['user_email'] = "testus"
        form['user_email_confirm'] = "testus"

        new_res = form.submit()
        res = new_res.follow()
        res.mustcontain("Invalid email address")

        form['user_email'] = "test@localhost"
        form['user_email_confirm'] = "test@test"

        new_res = form.submit()
        res = new_res.follow()
        res.mustcontain("Email address mismatch")

        form = None
        for key in res.forms.keys():
            if 'user_email' in res.forms[key].fields:
                form = res.forms[key]

        self.assertNotEqual(form, None)

        form['user_pass'] = "topsecret"

        new_res = form.submit()
        res = new_res.follow()
        res.mustcontain("Password mismatch")

        # finally do everything right

        form = None
        for key in res.forms.keys():
            if 'user_email' in res.forms[key].fields:
                form = res.forms[key]

        self.assertNotEqual(form, None)
        form['user_nick'] = "testus"

        new_res = form.submit()
        res = new_res.follow()
        res.mustcontain("Account information successfully updated")

        user = s.query(model.User).get(user.id)

        self.assertEqual(user.user_data.nick, u"testus")


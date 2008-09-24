import md5
from wombat.tests import *

class TestAuthController(TestController):

    def test_login(self):
        res = self.app.get(url_for(controller='auth', action='login', id=None))

        form = None
        for key in res.forms.keys():
            if 'email' in res.forms[key].fields:
                form = res.forms[key]

        self.assertNotEqual(form, None)

        form['email'] = "test@localhost"
        form['password'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("No such user")

        s = model.Session()
        # create the user as "inactive"
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()), False)
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        # test that disabled users can't log in
        form['email'] = "test@localhost"
        form['password'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Account disabled")

        user.active = True
        s.update(user)
        s.commit()

        form['email'] = "test@localhost"
        form['password'] = "test"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Password mismatch")

        form['email'] = "test@localhost"
        form['password'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("Welcome test@localhost")

    def test_check(self):
        res = self.app.get(url_for(controller='auth', action='check'))
        res.mustcontain("Not logged in")

        s = model.Session()
        # create a user that's already set "active"
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()), True)
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        res = self.app.post(url_for(controller='auth', action='submit', id='ajax'),
                params={'email':'test@localhost', 'password':'secret'})
        res.mustcontain("success")

        self.assertEqual(res.session['user'].email, u'test@localhost')

        res = self.app.get(url_for(controller='auth', action='check'))
        res.mustcontain("Logged in as test@localhost")

    def test_logout(self):
        # This should work without user
        res = self.app.get(url_for(controller='auth', action='logout'))
        res.mustcontain("logged out")

        # and with user
        s = model.Session()
        # create a user that's already active
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()), True)
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        res = self.app.post(url_for(controller='auth', action='submit', id='ajax'),
                params={'email':'test@localhost', 'password':'secret'})
        res.mustcontain("success")

        # This should work without user
        res = self.app.get(url_for(controller='auth', action='logout', id=None))
        res.mustcontain("logged out")


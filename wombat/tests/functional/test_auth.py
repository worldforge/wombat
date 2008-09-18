import md5
from wombat.tests import *

class TestAuthController(TestController):

    def test_login(self):
        res = self.app.get(url_for(controller='auth', action='login', id=None))

        form = res.forms[2]

        form['email'] = "test@localhost"
        form['password'] = "secret"
        new_res = form.submit()

        res = new_res.follow()
        res.mustcontain("No such user")

        s = model.Session()
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()))
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
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
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()))
        data = model.UserData(u"Test Testus", u"test", u"test", u"test")
        data.user = user
        s.save(user)
        s.save(data)
        s.commit()

        res = self.app.post(url_for(controller='auth', action='submit', id='ajax'),
                params={'email':'test@localhost', 'password':'secret'})
        res.mustcontain("success")

        self.assertEqual(res.session['user'], u'test@localhost')

        res = self.app.get(url_for(controller='auth', action='check'))
        res.mustcontain("Logged in as test@localhost")

    def test_logout(self):
        # This should work without user
        res = self.app.get(url_for(controller='auth', action='logout'))
        res.mustcontain("Logged out successfully")

        # and with user
        s = model.Session()
        user = model.User(u"test@localhost", unicode(md5.md5(u"secret").hexdigest()))
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
        res.mustcontain("Logged out successfully")


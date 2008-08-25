from wombat.tests import *
from datetime import datetime

class TestRevisionController(TestController):

    def test_show(self):
        # Test we're getting a 404 return for a revision not in the database
        response = self.app.get(url_for(controller='revision', action='show',
            id='1'), status=404)

        # Now create the revision and test again.
        s = model.Session()
        rev = model.Revision(1, u"r1", u"Test log message", u"kai",
                datetime.now().isoformat())
        s.save(rev)
        s.commit()
        response = self.app.get(url_for(controller='revision', action='show', id='1'))

        self.assertEqual(response.c.revision, rev)
        response.mustcontain("Test log message", "kai")

    def test_detail(self):
        # Test we're getting a 404 return for a revision not in the database
        response = self.app.get(url_for(controller='revision', action='show',
            id='1'), status=404)

        # Now create the revision and test again.
        s = model.Session()
        rev = model.Revision(1, u"r1", u"Test log message", u"kai",
                datetime.now().isoformat())
        s.save(rev)
        s.commit()
        response = self.app.get(url_for(controller='revision', action='show', id='1'))

        self.assertEqual(response.c.revision, rev)
        response.mustcontain("Test log message", "kai")






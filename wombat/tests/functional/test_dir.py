from wombat.tests import *
from datetime import datetime

class TestDirController(TestController):

    def test_index(self):
        # without directories in the db, dir/index should fail
        response = self.app.get(url_for(controller='dir'), status=404)

        s = model.Session()
        r = model.Revision(1, u"r1", u"Test revision", u"kai",
                datetime.now().isoformat().replace('T', ' '))
        s.save(r)
        d = model.Dir(u".", u"/", u"fake://repo/uri/")
        d.revision = r
        s.save(d)

        f1 = model.File(u"fake.png", u"fake.png", 1234, u"fake://repo/uri/")
        f1.revision = r
        f1.directory = d
        s.save(f1)

        sd = model.Dir(u"texts", u"texts",  u"fake://repo/uri/")
        sd.revision = r
        sd.parent = d
        s.save(sd)

        f2 = model.File(u"texts/fake.txt", u"fake.txt", 23, u"fake://repo/uri/")
        f2.revision = r
        f2.directory = sd
        s.save(f2)
        s.commit()

        # No path specified, we should get the '.' dir
        response = self.app.get(url_for(controller='dir'))

        self.assertEqual(response.c.req_path, u".")
        self.assertEqual(response.c.dir.path, d.path)
        self.assertEqual(response.c.groups.keys(), [u'text', u'image'])
        self.assertEqual(response.c.groups[u'text'], [])
        self.assertEqual(response.c.groups[u'image'], [f1])

        # Now try with path
        response = self.app.get(url_for(controller='dir'),
            params={'path':'texts'})

        self.assertEqual(response.c.req_path, u"texts")
        self.assertEqual(response.c.dir.path, sd.path)
        self.assertEqual(response.c.groups.keys(), [u'text', u'image'])
        self.assertEqual(response.c.groups[u'image'], [])
        self.assertEqual(response.c.groups[u'text'][0].path, f2.path)


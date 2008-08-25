from wombat.tests import *
from datetime import datetime

class TestFileController(TestController):

    def test_index(self):
        # Without files in the database, file/index should fail
        response = self.app.get(url_for(controller='file'), status=404)

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

        # With files in database but an empty path, file/index should fail
        response = self.app.get(url_for(controller='file'), status=404)

        # With a wrong path param, file/index should fail
        response = self.app.get(url_for(controller='file'),
                        params={'path':'foo.cmf'}, status=404)

        # With a correct path param, file/index should work
        response = self.app.get(url_for(controller='file'),
                        params={'path':'fake.png'})

        self.assertEqual(response.c.file.path, f1.path)

    def test_panel(self):
        # Without files in the database, file/panel should fail
        response = self.app.get(url_for(controller='file', action='panel'),
                        status=404)

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

        # With files in database but an empty path, file/panel should fail
        response = self.app.get(url_for(controller='file', action='panel'),
                        status=404)

        # With a wrong path param, file/panel should fail
        response = self.app.get(url_for(controller='file', action='panel'),
                        params={'path':'foo.cmf'}, status=404)

        # With a correct path param, file/panel should work
        response = self.app.get(url_for(controller='file', action='panel'),
                        params={'path':'texts/fake.txt'})

        self.assertEqual(response.c.file.path, f2.path)

    def test_unassigned(self):
        # Without files in the db, c.unassigned should be empty
        response = self.app.get(url_for(controller='file', action='unassigned'))
        self.assertEqual(response.c.unassigned, [])

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

        # Now we have two files, both unassigned.
        response = self.app.get(url_for(controller='file', action='unassigned'))
        self.assertEqual(len(response.c.unassigned), 2)

        a = model.Asset(u'text files', u'texts html fake')
        a.files.append(s.query(model.File).get(f2.path))
        s.save(a)
        s.commit()

        # Only f1 should still be unassigned.
        response = self.app.get(url_for(controller='file', action='unassigned'))
        self.assertEqual(len(response.c.unassigned), 1)
        self.assertEqual(response.c.unassigned[0].path, f1.path)


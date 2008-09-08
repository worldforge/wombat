from wombat.tests import *
from datetime import datetime

class TestShowController(TestController):

    def test_index(self):
        # Empty db, we should render the "please scan" message.
        response = self.app.get(url_for(controller='show'))
        response.mustcontain("Data not ready", "Please scan")

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
        s.commit()

        response = self.app.get(url_for(controller='show'))

        c = response.c
        self.assertEqual(c.repo_url, f1.root)
        self.assertEqual(c.total_size, f1.size)
        self.assertEqual(c.file_count, 1)
        self.assertEqual(c.avg_size, 1234)
        self.assertEqual(c.ext_string, u'.png')
        self.assertEqual(c.ext_count, 1)
        self.assertEqual(c.revision, r.id)
        self.assertEqual(c.asset_count, 0)
        self.assertEqual(c.collection_count, 0)

    def test_search(self):
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

        # A search without keywords should give no results
        response  = self.app.get(url_for(controller='show', action='search'))

        c = response.c
        self.assertEqual(c.needle, "")
        self.assertEqual(c.match_author, "")
        self.assertEqual(c.match_ext, "")
        self.assertEqual(c.match_date_in, "")
        self.assertEqual(c.match_date_out, "")
        self.assertEqual(c.found_files, [])
        self.assertEqual(c.found_dirs, [])


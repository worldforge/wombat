from wombat.tests import *

class TestAssetController(TestController):

    def test_index(self):
        # Without assets, c.assets should be empty
        response = self.app.get(url_for(controller='asset'))
        self.assertEqual(response.c.assets, [])

        a1 = model.Asset(u'asset 1', u'first keyword')
        a2 = model.Asset(u'asset 2', u'second keyword')
        s = model.Session()
        s.save(a1)
        s.save(a2)
        s.commit()
        response = self.app.get(url_for(controller='asset'))
        self.assertEqual(response.c.assets, [a1, a2])

    def test_show(self):
        # Check we get a 404 return for an asset not in the database
        response = self.app.get(url_for(controller='asset', action='show',
            id='1'), status=404)

        a = model.Asset(u'asset 1', u'first asset keywords')
        s = model.Session()
        s.save(a)
        s.commit()

        response = self.app.get(url_for(controller='asset', action='show',
            id='1'))
        self.assertEqual(response.c.asset, a)

    def test_details(self):
        # Check we get a 404 return for an asset not in the database
        response = self.app.get(url_for(controller='asset', action='show',
            id='1'), status=404)
        a = model.Asset(u'asset 1', u'first asset keywords')
        s = model.Session()
        s.save(a)
        s.commit()

        response = self.app.get(url_for(controller='asset', action='show',
            id='1'))
        self.assertEqual(response.c.asset, a)

    def test_new(self):
        response = self.app.get(url_for(controller='asset', action='new'))
        # forms[0] is the quick search, forms[1] is the advanced search
        form = response.forms[2]
        form['asset_name'] = "asset 3"
        form['asset_keywords'] = "third asset keywords"
        new_res = form.submit('commit')
        self.assertNotEqual(response, new_res)

        final_res = new_res.follow()

        s = model.Session()
        self.assertEqual(final_res.c.asset.name,
                s.query(model.Asset).get(1).name)
        self.assertEqual(final_res.c.asset.keywords,
                s.query(model.Asset).get(1).keywords)

    def test_edit(self):
        # Check we get a 404 return for an asset not in the database
        response = self.app.get(url_for(controller='asset', action='edit',
            id='1'), status=404)

        a = model.Asset(u'asset 1', u'old keywords')
        s = model.Session()
        s.save(a)
        s.commit()
        response = self.app.get(url_for(controller='asset', action='edit',
            id='1'))

        self.assertEqual(response.c.asset.name, a.name)
        self.assertEqual(response.c.asset.keywords, a.keywords)

        # forms[0] is the quick search, forms[1] is the advanced search
        form = response.forms[2]
        form['asset_keywords'] = u"new asset keywords"
        new_res = form.submit('commit')
        self.assertNotEqual(response, new_res)

        final_res = new_res.follow()
        self.assertEqual(final_res.c.asset.name, a.name)
        self.assertEqual(final_res.c.asset.keywords, u'new asset keywords')

    def test_delete(self):
        # Check we get a 404 return for an asset not in the database
        response = self.app.get(url_for(controller='asset', action='delete',
            id='1'), status=404)

        a = model.Asset(u'asset 1', u'first asset keywords')
        s = model.Session()
        s.save(a)
        s.commit()
        self.assertEqual(s.query(model.Asset).get(1), a)
        response = self.app.get(url_for(controller='asset', action='delete',
            id='1'))

        self.assertEqual(s.query(model.Asset).get(1), None)


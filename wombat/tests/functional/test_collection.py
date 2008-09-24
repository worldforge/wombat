from wombat.tests import *

class TestCollectionController(TestController):

    def test_index(self):
        # Without collections, c.collections should be empty
        response = self.app.get(url_for(controller='collection'))
        self.assertEqual(response.c.collections, [])

        c1 = model.Collection(u'collection 1', u'first keyword')
        c2 = model.Collection(u'collection 2', u'second keyword')
        s = model.Session()
        s.save(c1)
        s.save(c2)
        s.commit()
        response = self.app.get(url_for(controller='collection'))
        self.assertEqual(response.c.collections, [c1, c2])

    def test_show(self):
        # Check we get a 404 return for a collection not in the database
        response = self.app.get(url_for(controller='collection', action='show',
            id='1'), status=404)

        c = model.Collection(u'collection 1', u'first collection keywords')
        s = model.Session()
        s.save(c)
        s.commit()

        response = self.app.get(url_for(controller='collection', action='show',
            id='1'))
        self.assertEqual(response.c.collection, c)

    def test_details(self):
        # Check we get a 404 return for a collection not in the database
        response = self.app.get(url_for(controller='collection', action='show',
            id='1'), status=404)
        c = model.Collection(u'collection 1', u'first collection keywords')
        s = model.Session()
        s.save(c)
        s.commit()

        response = self.app.get(url_for(controller='collection', action='show',
            id='1'))
        self.assertEqual(response.c.collection, c)

    def test_new(self):
        response = self.app.get(url_for(controller='collection', action='new'))
        form = None
        for key in response.forms.keys():
            if 'collection_name' in response.forms[key].fields:
                form = response.forms[key]

        self.assertNotEqual(form, None)

        form['collection_name'] = "collection 3"
        form['collection_keywords'] = "third collection keywords"
        new_res = form.submit('commit')
        self.assertNotEqual(response, new_res)

        final_res = new_res.follow()

        s = model.Session()
        self.assertEqual(final_res.c.collection.name,
                s.query(model.Collection).get(1).name)
        self.assertEqual(final_res.c.collection.keywords,
                s.query(model.Collection).get(1).keywords)

    def test_edit(self):
        # Check we get a 404 return for a collection not in the database
        response = self.app.get(url_for(controller='collection', action='edit',
            id='1'), status=404)

        c = model.Collection(u'collection 1', u'old keywords')
        s = model.Session()
        s.save(c)
        s.commit()
        response = self.app.get(url_for(controller='collection', action='edit',
            id='1'))

        self.assertEqual(response.c.collection.name, c.name)
        self.assertEqual(response.c.collection.keywords, c.keywords)
        for key in response.forms.keys():
            if 'collection_keywords' in response.forms[key].fields:
                form = response.forms[key]

        self.assertNotEqual(form, None)

        form['collection_keywords'] = u"new collection keywords"
        new_res = form.submit('commit')
        self.assertNotEqual(response, new_res)

        final_res = new_res.follow()
        self.assertEqual(final_res.c.collection.name, c.name)
        self.assertEqual(final_res.c.collection.keywords, u'new collection keywords')

    def test_delete(self):
        # Check we get a 404 return for a collection not in the database
        response = self.app.get(url_for(controller='collection', action='delete',
            id='1'), status=404)

        c = model.Collection(u'collection 1', u'first collection keywords')
        s = model.Session()
        s.save(c)
        s.commit()
        self.assertEqual(s.query(model.Collection).get(1), c)
        response = self.app.get(url_for(controller='collection', action='delete',
            id='1'))

        self.assertEqual(s.query(model.Collection).get(1), None)


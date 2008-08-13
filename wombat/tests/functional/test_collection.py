from wombat.tests import *

class TestCollectionController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='collection'))
        # Test response...

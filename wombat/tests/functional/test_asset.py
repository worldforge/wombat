from wombat.tests import *

class TestAssetController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='asset'))
        # Test response...

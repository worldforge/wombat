from wombat.tests import *

class TestScanController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='scan'))
        # Test response...

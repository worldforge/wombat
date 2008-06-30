from wombat.tests import *

class TestShowController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='show'))
        # Test response...

from wombat.tests import *

class TestRevisionController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='revision'))
        # Test response...

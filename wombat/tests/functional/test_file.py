from wombat.tests import *

class TestFileController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='file'))
        # Test response...

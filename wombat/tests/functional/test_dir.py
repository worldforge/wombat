from wombat.tests import *

class TestDirController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='dir'))
        # Test response...

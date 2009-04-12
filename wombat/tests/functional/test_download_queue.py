from wombat.tests import *

class TestDownloadQueueController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='download_queue', action='index'))
        # Test response...

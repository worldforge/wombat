"""The application's Globals object"""
from pylons import config
from threading import Timer, Lock
from wombat.lib.cleanup import cleanup_dbs
from wombat.lib.update import update_media

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.version = "0.4.2"

        self.last_cleanup = "Never"
        self.cleanup_timer = Timer(60.0, cleanup_dbs, [self])
        self.cleanup_timer.start()

        self.scan_lock = Lock()

        self.update_status = "Never updated"
        self.update_timer = Timer(30.0, update_media, [self])
        self.update_timer.start()

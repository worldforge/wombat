"""Setup the wombat application"""
import logging
import sys
from pylons import config

from wombat.config.environment import load_environment
from wombat.model import meta
from wombat.lib.auth import crypt_password

log = logging.getLogger(__name__)

def setup_superuser(model):
    """Set up the superuser account"""
    s = meta.Session()
    print "Enter email for the super user"
    email = unicode(sys.stdin.readline().strip())
    print "Enter superuser password"
    passwd = crypt_password(sys.stdin.readline().strip())
    user = model.User(email, passwd, True)
    admin = s.query(model.Role).filter_by(name=u"admin").first()
    if admin is not None:
        user.roles.append(admin)
    s.add(user)
    data = model.UserData(u"System Administrator", u"admin")
    data.user = user
    s.add(data)
    s.commit()

def create_roles(model):
    """Create the default roles"""
    s = meta.Session()
    admin = model.Role(u"admin")
    lead = model.Role(u"lead")
    artist = model.Role(u"artist")
    s.add(admin)
    s.add(lead)
    s.add(artist)
    s.commit()

def setup_app(command, conf, vars):
    """Place any commands to setup wombat here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create cache dir, if it doesn't exist yet
    import os
    import os.path
    if not os.path.exists(config['app_conf']['cache_dir']):
        os.makedirs(config['app_conf']['cache_dir'])

    # Populate the DB on 'paster setup-app'
    import wombat.model as model
    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    create_roles(model)

    answer = ""

    if config['app_conf']['create_superuser'] == "false":
        answer = "n"

    while not answer in ("y", "n"):
        print "Set up superuser account now? (Y/N)"
        answer = sys.stdin.readline().strip().lower()

    if answer == "y":
        setup_superuser(model)



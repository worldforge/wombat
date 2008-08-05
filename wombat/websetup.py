"""Setup the wombat application"""
import logging

from paste.deploy import appconfig
from pylons import config

from wombat.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup wombat here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)

    # Create cache dir, if it doesn't exist yet
    import os
    import os.path
    if not os.path.exists(config['app_conf']['cache_dir']):
        os.makedirs(config['app_conf']['cache_dir'])

    # Populate the DB on 'paster setup-app'
    import wombat.model as model

    log.info("Setting up database connectivity...")
    engine = config['pylons.g'].sa_engine
    log.info("Creating tables...")
    model.metadata.create_all(bind=engine)
    log.info("Successfully set up.")


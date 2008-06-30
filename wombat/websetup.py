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

import site
site.addsitedir('/home/wombat/lib/python2.4/site-packages')
import os, sys
sys.path.append('/home/wombat/wsgi/wombat')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-eggs'

from paste.deploy import loadapp

application = loadapp('config:/home/wombat/wsgi/wombat.ini')


import os
import sys
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(__file__))

import atexit
import threading
import cherrypy
from etc import cherrypy_global_config_file, cherrypy_nonlocal_config_file, cherrypy_local_config_file, cherrypy_config_file
from inventoryserver.server import InventoryServer
from inventoryserver.server import Register
from inventoryserver.server import Admin
from inventoryserver.server import Noteboard

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

class Root(object):
    def index(self):
        return 'Hello World!'
    index.exposed = True

root=InventoryServer()
root.admin=Admin()
root.notes=Noteboard()
root.register=Register()

application = cherrypy.Application(root, script_name=None, config=cherrypy_local_config_file)



import os
import sys
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(__file__))

import atexit
import threading
import cherrypy

from config.etc import cherrypy_nonlocal_config_file, client_side_logging_enabled

from inventoryserver.server import InventoryServer
from inventoryserver.server import Register
from inventoryserver.server import Admin
from inventoryserver.server import Staffing
from inventoryserver.server import Noteboard
from inventoryserver.server import SpecialOrders
from inventoryserver.server import CSLogging

#cherrypy.config.update({'environment': 'embedded'})
cherrypy.config.update({'tools.sessions.on': True})

#if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
#    cherrypy.engine.start(blocking=False)
#    atexit.register(cherrypy.engine.stop)

class Root(object):
    def index(self):
        return 'Hello World!'
    index.exposed = True

root=InventoryServer()
root.admin=Admin()
root.staffing=Staffing()
root.notes=Noteboard()
root.register=Register()
root.specialorder=SpecialOrders()

#if client_side_logging_enabled:
#    root.logging=CSLogging()

#application = cherrypy.Application(root, script_name=None, config=cherrypy_nonlocal_config_file)
application = cherrypy.Application(root)

import os
import sys
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(__file__))

import atexit
import threading
import cherrypy
from config.etc import cherrypy_local_config_file

from inventoryserver.server import InventoryServer
from inventoryserver.server import Register
from inventoryserver.server import Admin
from inventoryserver.server import Staffing
from inventoryserver.server import Noteboard
from inventoryserver.server import SpecialOrders

cherrypy.config.update({'tools.sessions.on': True})
cherrypy.config.update({'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession})
cherrypy.config.update({'tools.sessions.storage_path': "/var/www/isk-production/infoshopkeeper/sessions"})
cherrypy.config.update({'tools.sessions.timeout': 60})

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

application = cherrypy.Application(root)

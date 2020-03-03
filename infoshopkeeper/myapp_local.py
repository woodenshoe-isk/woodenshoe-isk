import os
import sys

sys.stdout = sys.stderr
sys.path.append(os.path.dirname(__file__))

import atexit
import threading
import cherrypy

from config.config import configuration

from inventoryserver.server import InventoryServer
from inventoryserver.server import Register
from inventoryserver.server import Admin
from inventoryserver.server import Staffing
from inventoryserver.server import Noteboard
from inventoryserver.server import SpecialOrders

# cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith("3.0") and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)


class Root(object):
    def index(self):
        return "Hello World!"

    index.exposed = True


root = InventoryServer()
root.admin = Admin()
root.staffing = Staffing()
root.notes = Noteboard()
root.register = Register()
root.specialorder = SpecialOrders()

cherrypy_local_config_file = configuration.get("cherrypy_local_config_file")
application = cherrypy.Application(
    root, script_name=None, config=cherrypy_local_config_file
)

if __name__ == "__main__":
    cherrypy.quickstart(root, "/", cherrypy_local_config_file)

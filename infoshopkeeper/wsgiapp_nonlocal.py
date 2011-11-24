import os
import sys
sys.stdout = sys.stderr
sys.path.append(os.path.dirname(__file__))

import atexit
import threading
import cherrypy

from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.evalexception import EvalException

from etc import cherrypy_global_config_file, cherrypy_nonlocal_config_file, cherrypy_local_config_file, cherrypy_config_file

from inventoryserver.server import InventoryServer
from inventoryserver.server import Noteboard

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

root=InventoryServer()
root.notes=Noteboard()

#root=ErrorMiddlware(root, debug=True)
#application=ErrorMiddleware(app, debug=True, show_exceptions_in_wsgi_errors=True)
app=cherrypy.Application(root, script_name=None, config=cherrypy_local_config_file)
application=EvalException(app)

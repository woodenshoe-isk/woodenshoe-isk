#!/usr/bin/python

import os
import cherrypy
from etc import cherrypy_global_config_file, cherrypy_nonlocal_config_file, cherrypy_local_config_file, cherrypy_config_file
from inventoryserver.server import InventoryServer
from inventoryserver.server import Register

#
# Specify a logfile as soon as possible so we increase the chance of logging
# errors. This could be commented out once the application works on the live
# server under mod_python
#
cherrypy.config['log.error_file'] = '/home/tech/Developer/infoshopkeeper/error.log'

#
# Our actual (dummy) web application
#
class DVD:
    def index(self, sort = None, edit_id = None):
        return('Hello world!')
    index.exposed = True

#
# Set up cherrypy so it's independent of the path being run from, and load the
# configuration.
#
path_base = os.path.dirname(__file__)
#path_config = os.path.join(path_base, 'dvd.ini')
#path_db = os.path.join(path_base, 'dvd.db')

#cherrypy.config.update(path_config)

#
# Set up stuff for our application to use.
#
#metadata = sqlalchemy.BoundMetaData('sqlite://%s' % (path_db))

#
# These methods take care of running the application via either mod_python or
# stand-alone using the built-in CherryPy server.
#
def start_modpython():
    #print "in start_modpython"
    cherrypy.engine.SIGHUP = None
    cherrypy.engine.SIGTERM = None
    cherrypy.tree.mount(DVD(), config=cherrypy_global_config_file)
    cherrypy.engine.start(blocking=False)

def start_standalone():
    cherrypy.quickstart(DVD()) #, config=cherrypy_global_config_file)

#
# If we're not being imported, it means we should be running stand-alone.
#
if __name__ == '__main__':
    start_standalone()

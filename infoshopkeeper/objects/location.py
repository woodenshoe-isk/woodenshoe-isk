import sys

from sqlobject import *
from tools import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Location(SQLObjectWithFormGlue):
	_connection = db.conn() 
	class sqlmeta:
		fromDatabase = True





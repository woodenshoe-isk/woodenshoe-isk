import sys

from sqlobject import *
from tools import db

from SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Kind(SQLObjectWithFormGlue):
	_connection = db.conn()
	titles=MultipleJoin('Title')
	class sqlmeta:
		fromDatabase = True





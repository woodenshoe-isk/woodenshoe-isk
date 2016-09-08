from sqlobject import *
from tools import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from datetime import datetime
from mx import DateTime

class Notes(SQLObjectWithFormGlue):
	whenEntered=DateTimeCol(dbName='whenEntered', default=datetime.now)
	class sqlmeta:
  	    fromDatabase = True
	_connection = db.conn()

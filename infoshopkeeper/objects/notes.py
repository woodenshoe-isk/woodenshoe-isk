from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx import DateTime

class Notes(SQLObjectWithFormGlue):
	whenEntered=DateTimeCol(dbName='whenEntered', default=DateTime.now)
	class sqlmeta:
  	    fromDatabase = True
	_connection = db.conn()

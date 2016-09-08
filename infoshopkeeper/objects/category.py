from sqlobject import *
from tools import db
from objects.title import Title
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Category(SQLObjectWithFormGlue):
	_connection = db.conn() 
	title = ForeignKey('Title')

	class sqlmeta:
		fromDatabase = True


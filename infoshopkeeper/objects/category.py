from sqlobject import *
from tools import db
from objects.title import Title
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Category(SQLObjectWithFormGlue):
	title = ForeignKey('Title')

	class sqlmeta:
		fromDatabase = True


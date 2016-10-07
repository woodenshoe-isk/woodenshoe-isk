from sqlobject import *
from tools import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx import DateTime

class ISBN_to_be_entered(SQLObjectWithFormGlue):
	class sqlmeta:
  	    fromDatabase = True
            table = 'ISBN_to_be_entered'

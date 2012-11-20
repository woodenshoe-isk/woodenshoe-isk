from components import db
from mx import DateTime
from objects.specialorder import SpecialOrder
from objects.title import Title
from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

class TitleSpecialOrder(SQLObjectWithFormGlue):
	orderStatus=EnumCol(enumValues=(u'ON ORDER', u'ON HOLD SHELF', u'COMPLETE'), default=u'ON ORDER', dbName='order_status')
	specialOrder=ForeignKey('SpecialOrder', dbName='special_order_id')
	title=ForeignKey('Title')

	class sqlmeta:
  	    fromDatabase = True
  	    table = 'title_special_order'
	_connection = db.conn()

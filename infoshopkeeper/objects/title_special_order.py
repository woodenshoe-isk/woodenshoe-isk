from tools import db
from mx import DateTime
from objects.special_order import SpecialOrder
from objects.title import Title
from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

class TitleSpecialOrder(SQLObjectWithFormGlue):
	orderStatus=EnumCol(enumValues=(u'PENDING', u'ON ORDER', u'ON HOLD SHELF', u'UNAVAILABLE', u'SOLD', u'RETURNED TO SHELVES'), default=u'ON ORDER', dbName='order_status')
	specialOrder=ForeignKey('SpecialOrder', dbName='special_order_id')
	title=ForeignKey('Title')

	class sqlmeta:
  	    fromDatabase = True
  	    table = 'title_special_order'
	_connection = db.conn()

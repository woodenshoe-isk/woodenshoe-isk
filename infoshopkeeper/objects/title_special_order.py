from tools import db
from mx import DateTime
from objects.special_order import SpecialOrder
from objects.title import Title
from sqlobject import *
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue

class TitleSpecialOrder(SQLObjectWithFormGlue):
	orderStatus=EnumCol(enumValues=('PENDING', 'ON ORDER', 'ON HOLD SHELF', 'UNAVAILABLE', 'SOLD', 'RETURNED TO SHELVES'), default='ON ORDER', dbName='order_status')
	specialOrder=ForeignKey('SpecialOrder', dbName='special_order_id')
	title=ForeignKey('Title')

	class sqlmeta:
  	    fromDatabase = True
  	    table = 'title_special_order'

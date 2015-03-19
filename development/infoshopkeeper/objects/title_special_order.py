from components import db
from mx import DateTime
from objects.special_order import SpecialOrder
from objects.title import Title
from mx.DateTime import now
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from sqlobject import *

class TitleSpecialOrder(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True
        table = 'title_special_order'
    _connection = db.conn()
    readOnlyColumns=('placedWhen', 'orderedWhen', 'arrivedWhen', 'finishedWhen')
    
    orderStatus=EnumCol(enumValues=(u'PENDING', u'ON ORDER', u'ON HOLD SHELF', u'UNAVAILABLE', u'PICKED UP', u'RETURNED TO SHELVES'), default=u'PENDING', dbName='order_status')
    specialOrder=ForeignKey('SpecialOrder', dbName='special_order_id')
    title=ForeignKey('Title')
    
    def _set_orderStatus(self, value):
        if value == u'PENDING':
            self.placedWhen=now()
            self.orderedWhen = self.arrivedWhen =self.finishedWhen = None
        elif value == u'ON ORDER':
            self.orderedWhen=now()
            self.arrivedWhen = self.finishedWhen = None
        elif value == u'ON HOLD SHELF':
            self.arrivedWhen = now()
            self.finishedWhen = None
        elif value in (u'UNAVAILABLE', u'PICKED UP', u'RETURNED TO SHELVES'):
            self.finishedWhen = now()
        self._SO_set_orderStatus(value)

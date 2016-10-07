import sys
import string

from objects.title import Title
from objects.location import Location
from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now

from tools import db

class Book(SQLObjectWithFormGlue):
    listprice=FloatCol()
    ourprice=FloatCol()
    inventoried_when=DateCol(default=now)
    sold_when=DateCol(default=now)  # we ignore this until the status gets set to "SOLD"  
    status = EnumCol(enumValues=(u'STOCK', u'SOLD', u'NOT FOUND'), default=u"STOCK")
    consignmentStatus = StringCol()            
    distributor =StringCol()
    #location = StringCol()
    owner =StringCol()
    notes =StringCol()

    location = ForeignKey('Location')
    listTheseKeys=('location')
    sortTheseKeys='locationName'
 
    title = ForeignKey('Title')

    #we link changes of status to change in sold_when date
    def _set_status(self, value):
        if value in ('SOLD', 'NOT FOUND'):
            self.sold_when=now()
        elif value == 'STOCK':
            self.sold_when=self.inventoried_when
        self._SO_set_status(value)


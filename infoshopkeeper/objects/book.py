import sys
import string

from objects.title import Title
from objects.location import Location
from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now

from components import db
from config import configuration
cfg = configuration()

#_connection = db.SQLObjconnect()

class Book(SQLObjectWithFormGlue):
    _connection = db.conn() 
    listprice=FloatCol()
    ourprice=FloatCol()
    inventoried_when=DateCol(default=now)
    sold_when=DateCol(default=now)  # we ignore this until the status gets set to "SOLD"  
    status = EnumCol(enumValues=(u'STOCK', u'SOLD', u'DELETED'), default=u"STOCK")
    consignmentStatus = StringCol()            
    distributor =StringCol()
    #location = StringCol()
    owner =StringCol()
    notes =StringCol()

    location = ForeignKey('Location')
    listTheseKeys=('location')
    sortTheseKeys='locationName'
 

    title = ForeignKey('Title')
    multiplied=False

    def getTitle(self):
                return self.title
    
    def object_to_form(self):
        self.extracolumns()
        return SQLObjectWithFormGlue.object_to_form(self)

    def extracolumns(self):
        if not(self.multiplied):
            for mp in cfg.get("multiple_prices"):
                self.sqlmeta.addColumn(FloatCol(string.replace(mp[0]," ",""),default=0))
            self.multiplied=True
    
    def sellme(self):
        self.status="SOLD"
        self.sold_when=now()

    def change_status(self,new_status):
        self.status=new_status
    
    def _set_status(self, value):
        if value in ('SOLD', 'DELETED'):
            self.sold_when=now()
        elif value == 'STOCK':
            self.sold_when=self.inventoried_when
        self._SO_set_status(value)

   
    def _set_status(self, value):
        if value in ('SOLD', 'DELETED'):
            self.sold_when=now()
        elif value == 'STOCK':
            self.sold_when=self.inventoried_when
        self._SO_set_status(value)




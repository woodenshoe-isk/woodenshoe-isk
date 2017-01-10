import sys
import string


from sqlobject import *
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue
import datetime


from tools import db
from tools.now import Now

#_connection = db.SQLObjconnect()

class Transaction(SQLObjectWithFormGlue):

    class sqlmeta:
        from_database=True
        table = "transactionLog"
    
    action=StringCol()
    amount=FloatCol()
    date=DateTimeCol(default=Now.now)
    schedule = StringCol()            
    info =StringCol()
    owner =StringCol()
    cashier =StringCol()
    cartID=StringCol()

    def object_to_form(self):
        self.extracolumns()
        return SQLObjectWithFormGlue.object_to_form(self)

    def extracolumns(self):
        pass

    def void(self):
        pass

    def get_info(self):
        if 'tostring' in dir(self.info):
            return self.info.tostring()
        else:
            return self.info

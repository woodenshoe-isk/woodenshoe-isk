from sqlobject import *
from tools import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx import DateTime
from Crypto.Cipher import AES
from config.etc import db_col_password as password

class SpecialOrder(SQLObjectWithFormGlue):
    _connection = db.conn()
    _aes = AES.new( password + (16- (password.__len__() % 16))*'{') 

    dateOrdered=DateTimeCol(dbName='date_ordered', default=DateTime.now)
    titles = RelatedJoin('Title', intermediateTable='title_special_order',createRelatedTable=False)    
    title_pivots = MultipleJoin('TitleSpecialOrder')
    class sqlmeta:
        fromDatabase = True

    def _get_contactInfo(self):
        return self._SO_get_contactInfo()
    
    def _set_contactInfo(self,value):
        self._SO_set_contactInfo(value)
    
    def _get_customerName(self):
        return self._SO_get_customerName()
    
    def _set_customerName(self,value):
        self._SO_set_customerName(value)
        

from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from sqlobject import *
from objects.title import Title
from mx.DateTime import now

from components import db
from Crypto.Cipher import AES
from etc import db_col_password as password

class SpecialOrder( SQLObjectWithFormGlue ):
    _connection = db.conn()
    _aes = AES.new( password + (16- (password.__len__() % 16))*'{', AES.MODE_CBC) 
    
    class sqlmeta:
        fromDatabase=True
        
    orderedWhen=DateCol(default=now)
    status=EnumCol( enumValues = (u'PENDING', u'ORDERED', u'ON HOLD', u'UNAVAILABLE', u'SOLD', u'RETURNED TO SHELVES'), default = u'PENDING')
    title = ForeignKey('Title')
    
    def _get_customerContactInfo(self):
        encrypted_data = self._SO_get_customerContactInfo()
        data = SpecialOrder._aes.decrypt( encrypted_data.decode('base64') )
        return data.lstrip('}').rstrip('{')
    
    def _set_customerContactInfo(self,value):
        encrypted_value = SpecialOrder._aes.encrypt(16*'}' + value + (16 - (value.__len__() % 16))*'{')
        self._SO_set_customerContactInfo(encrypted_value.encode('base64'))
    
    def _get_customerName(self):
        encrypted_data = self._SO_get_customerName()
        data = SpecialOrder._aes.decrypt( encrypted_data.decode('base64') )
        return data.lstrip('}').rstrip('{')

    
    def _set_customerName(self,value):
        encrypted_value = SpecialOrder._aes.encrypt(16*'}' + value + (16 - (value.__len__() % 16))*'{')
        self._SO_set_customerName(encrypted_value.encode('base64'))
        
    
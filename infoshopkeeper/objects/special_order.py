from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from sqlobject import *
from objects.title import Title
from mx.DateTime import now

from components import db
import etc

class SpecialOrder( SQLObjectWithFormGlue ):
    _connection = db.conn()
    
    class sqlmeta:
        fromDatabase=True
        
    ordered_when=DateTimeCol(default=now)
    title = ForeignKey('Title')
    
    def _get_contactInfo(self):
        return self._SO_get_contactInfo()
    
    def _set_contactInfo(self,value):
        self._SO_set_contactInfo(value)
    
    def _get_customerName(self):
        return self._SO_get_customerName()
    
    def _set_customerName(self,value):
        self._SO_set_customerName(value)
        
    
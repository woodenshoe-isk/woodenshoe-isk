from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx import DateTime

class Title_SpecialOrder(SQLObjectWithFormGlue):
    class sqlmeta:
        table='title_special_order'
    title = ForeignKey('Title', notNull=True, cascade=True)
    special_order = ForeignKey('SpecialOrder', notNull=True, cascade=True)    
    
from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx import DateTime

class SpecialOrder(SQLObjectWithFormGlue):
    dateOrdered=DateTimeCol(dbName='date_ordered', default=DateTime.now)
    titles = RelatedJoin('Title', intermediateTable='title_special_order',createRelatedTable=False)    
    title_pivots = MultipleJoin('TitleSpecialOrder')
    class sqlmeta:
        fromDatabase = True
    _connection = db.conn()

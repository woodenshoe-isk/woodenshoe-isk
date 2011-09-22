import sys
sys.path.append("/home/woodenshoe/infoshopkeeper/")

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Author(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True

    _connection = db.conn() 
    authorName=UnicodeCol(default=None)
    title = RelatedJoin('Title', intermediateTable='author_title',createRelatedTable=True)

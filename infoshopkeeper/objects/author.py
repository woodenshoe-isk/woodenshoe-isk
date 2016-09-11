from sqlobject import *
from tools import db
from objects.title import Title

from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Author(SQLObjectWithFormGlue):
    class sqlmeta:
        fromDatabase = True

    _connection = db.conn() 
    authorName=UnicodeCol(default=None)
    title = RelatedJoin('Title', intermediateTable='author_title',createRelatedTable=True)

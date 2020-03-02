from sqlobject import *
from tools import db, now
from .SQLObjectWithFormGlue import SQLObjectWithFormGlue
from datetime import datetime


class Notes(SQLObjectWithFormGlue):
    whenEntered = DateTimeCol(dbName="whenEntered", default=now.Now.now)

    class sqlmeta:
        fromDatabase = True

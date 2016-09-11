from sqlobject import *
from tools import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Member(SQLObjectWithFormGlue):
    _connection = db.conn() 
    first_name = StringCol()
    last_name = StringCol()
    e_mail = StringCol()
    phone = StringCol()
    paid = StringCol()

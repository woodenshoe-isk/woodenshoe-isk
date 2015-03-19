from sqlobject import SQLObject

class MySQLObject(SQLObject):
    def __init__(self, *args, **kwargs):
        super(MySQLObject, self).__init__(*args, **kwargs)

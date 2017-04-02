import datetime

class NowType(type):
    @property
    def now(cls):
        return datetime.datetime.now()
        
class Now(metaclass=NowType):
    pass
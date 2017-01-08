from logging.handlers import RotatingFileHandler
import os

class GroupRotatingFileHandler(RotatingFileHandler):    
    def _open(self):
        prevumask=os.umask(0o002)
        if self.encoding is None:
            stream = open(self.baseFilename, self.mode)
        else:
            stream = codecs.open(self.baseFilename, self.mode, self.encoding)
        ##os.fdopen(os.open('/path/to/file', os.O_WRONLY, 0600))
        rtv=RotatingFileHandler._open(self)
        os.umask(prevumask)
        return stream

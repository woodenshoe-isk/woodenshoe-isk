from config import configuration
from inventoryserver.server import *
import Cheetah

class SkeletonBase(Cheetah.Template.Template):
    def __init__(self, *args, **kwargs):
        super(SkeletonBase, self).__init__(*args, **kwargs)
        self.reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in configuration().get("reports")]
        self.reports=[r.metadata for r in self.reportlist]
        self.menudata=MenuData


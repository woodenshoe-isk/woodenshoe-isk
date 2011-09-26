from config import configuration
import Cheetah

cfg=configuration()

class SkeletonBase(Cheetah.Template.Template):
    def __init__(self, *args, **kwargs):
        super(SkeletonBase, self).__init__(*args, **kwargs)
        self.reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in cfg.get("reports")]
        self.reports=[r.metadata for r in self.reportlist]


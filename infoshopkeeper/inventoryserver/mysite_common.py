from config.config import configuration

cfg=configuration()

class mysite_common(object):
    reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in cfg.get("reports")]
    reports=[r.metadata for r in reportlist]

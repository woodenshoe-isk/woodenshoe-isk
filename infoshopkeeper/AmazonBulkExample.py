from etc import *
from ecs import *
from objects.book import *
from sqlobject.sqlbuilder import *

setLicenseKey(amazon_license_key)
setSecretAccessKey(amazon_secret_key)
setAssociateTag(amazon_associate_tag)

titles=Title.select(RLIKE(Title.q.isbn, "^[0-9]{13}$"))
for t in titles:
    try:
        amazonIter=ItemLookup(t.isbn, ResponseGroup="ItemAttributes")
        amazonResults=amazonIter.next()
        t.set(type=amazonResults.Binding)
    except:
        pass


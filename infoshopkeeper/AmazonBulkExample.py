from etc import *
from ecs import *
from objects.book import *
from sqlobject.sqlbuilder import *
import time

setLicenseKey(amazon_license_key)
setSecretAccessKey(amazon_secret_key)
setAssociateTag(amazon_associate_tag)


titles=Title.select(AND(RLIKE(Title.q.isbn, "^[0-9]{13}$"), RLIKE(Title.q.type, '^[^:alnum:]*$')))
for t in titles:
    try:
        amazonIter=ItemLookup(t.isbn, IdType='EAN', SearchIndex="Books", ResponseGroup="ItemAttributes")
        amazonResults=amazonIter.next()
        t.set(type=amazonResults.Binding)
        print t
        print amazonResults.Binding
    except Exception as excep:
        print excep
        pass
    time.sleep(1)

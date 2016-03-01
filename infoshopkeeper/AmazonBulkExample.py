from etc import *
from ecs import *
from objects.book import *
from objects.images import *

from sqlobject.sqlbuilder import *
import time

setLicenseKey(amazon_license_key)
setSecretAccessKey(amazon_secret_key)
setAssociateTag(amazon_associate_tag)


titles=Title.select(AND(RLIKE(Title.q.isbn, "^[0-9]{13}$"), Title.q.kindID==1))
for t in titles:
    try:
        amazonIter=ItemLookup(t.isbn, IdType='EAN', SearchIndex="Books", ResponseGroup="ItemAttributes,Images")
        amazonResults=amazonIter.next()
        if t.images:
            if not t.images.largeUrl:
                t.images.largeUrl = amazonResults.LargeImage.URL
            if not t.images.medUrl:
                t.images.medUrl = amazonResults.MediumImage.URL
            if not t.images.smallUrl:
                t.images.smallUrl = amazonResults.SmallImage.URL
        else:
            Images(titleID=t.id, largeUrl = amazonResults.LargeImage.URL, medUrl = amazonResults.MediumImage.URL, smallUrl = amazonResults.SmallImage.URL)
        print t    
    except Exception as excep:
        print excep
        pass
    time.sleep(1)

from etc import *
from ecs import *
from objects.book import *
from sqlobject.sqlbuilder import *

import re
import sys
import time


setLicenseKey(amazon_license_key)
setSecretAccessKey(amazon_secret_key)
setAssociateTag(amazon_associate_tag)

titles=Title.select(AND(RLIKE(Title.q.isbn, "^[0-9]{9}[0-9xX]$"), ISNULL(Title.q.orig_isbn)))

for t in titles:
    try:
        amazonIter=ItemLookup(t.isbn, ResponseGroup="ItemAttributes")
        amazonResults=amazonIter.next()
        amazonstring=' '.join(re.findall('\w{4,}', amazonResults.Title)[0:2]).lower()
        titlestring=' '.join(re.findall('\w{4,}', t.booktitle)[0:2]).lower()
        if titlestring == amazonstring:
            print "ISBN-13 is now ", amazonResults.EAN
            t.orig_isbn = amazonResults.EAN
    except:
        pass
    time.sleep(1)
    
titles=Title.select(AND(RLIKE(Title.q.isbn, "^[0-9]{9}[0-9xX]$"), ISNULL(Title.q.orig_isbn)))

for t in titles:
    try:
        amazonIter=ItemLookup(t.isbn, ResponseGroup="ItemAttributes")
        amazonResults=amazonIter.next()
        amazonstring=' '.join(re.findall('\w{4,}', amazonResults.Title)[0:2]).lower()
        titlestring=' '.join(re.findall('\w{4,}', t.booktitle)[0:2]).lower()
        if titlestring != amazonstring:
            print "Amazon:   ", amazonResults.Title
            print "Database: ", t.booktitle
            right_title_result = raw_input("Is this the right amazon title?")
            if ( right_title_result.lower() =='y'):
                print "ISBN-13 is now ", amazonResults.EAN
                t.orig_isbn = amazonResults.EAN
                substitute_title_result = raw_input('Should I substitute Amazon\'s for yours?')
                if ( substitute_title_result.lower() == 'y'):
                    print "New booktitle is now: ", amazonResults.Title
                    t.booktitle = amazonResults.Title
            if (right_title_result.lower() == 'q'):
                sys.exit(0)
        else:
            print "ISBN-13 is now ", amazonResults.EAN
            t.orig_isbn = amazonResults.EAN
    except SystemExit:
        sys.exit(0)
    except Exception as e:
        print e
	pass
    time.sleep(1)


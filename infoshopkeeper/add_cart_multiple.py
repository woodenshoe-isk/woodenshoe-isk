import json
import os
import random
import sys
import unittest
import webtest

from objects.book import Book

from wsgiapp_local import application

try:
    _my_app=webtest.TestApp(application)
except Exception as excp:
    sys.exit(0)

oldstderr=sys.stderr
oldstdout=sys.stdout

sys.stderr = sys.stdout = open(os.devnull, 'w')
random_app_urls=['/notes/noteboard', '/report?what=&begin_date=2012-01-01&end_date=2012-01-08&query_made=yes&reportname=salesreport', '/admin/kindlist']    
assertion_errcount=0
for j in range(1, 100):
    for i in range(1, 10):
        random_item=random.sample(list(Book.selectBy(status='STOCK')), 1)[0]
        item={"department":"Book","isInventoried":"True","isTaxable":"True","booktitle":random_item.title.booktitle,"isbn":random_item.title.isbn,"bookID":random_item.id,"titleID":random_item.titleID,"ourprice":random_item.ourprice}
        result=_my_app.post('/register/add_item_to_cart', {'item':json.dumps(item)})
        for k in range(0, random.randint(0,5)):
            _my_app.get(random.choice(random_app_urls))
        confirm=_my_app.get('/register/get_cart').json[0]['items']
        #print "test_add_inventoried", result, confirm
        try:
            assert i == len(confirm), '/register/add_item_to_cart dropped item'
        except:
            print >> oldstdout, i, len(confirm)
            assertion_errcount = assertion_errcount +1
    _my_app.get('/register/void_cart')

sys.stdout=oldstdout
sys.stderr=oldstderr

print "Count of assertion errors: ", assertion_errcount

sys.exit(0)
    

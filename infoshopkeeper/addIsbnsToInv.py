from components.inventory import inventory

from etc import *

from sqlobject import *

#Set up db connection
connection = connectionForURI('mysql://%s:%s@%s:3306/%s?debug=1&logger=MyLogger&loglevel=debug&use_unicode=1&charset=utf8' % (dbuser,dbpass,dbhost,dbname))
sqlhub.processConnection = connection

class ISBNToBeEntered(SQLObject):
    class sqlmeta:
        fromDatabase = True
	table = "ISBN_to_be_entered"

inv=inventory()
titles=ISBNToBeEntered.select()
for t in titles:
    #print t
    if len(t.isbn)!=13:
        continue
    try:
    	titleinfo=inv.lookup_by_isbn(t.isbn)
    except Exception as e:
        #print "isbn %s seems to be invalid" % t.isbn
        raise e
    if titleinfo:
        print titleinfo
        if titleinfo['kind'] != 'books':
            continue
        #print titleinfo
        if isinstance(titleinfo['list_price'],unicode):
	    correctedprice=float(titleinfo['list_price'].replace('$',''))
        elif not titleinfo['list_price']:
            correctedprice=0.0
        else:
	    correctedprice=float(titleinfo['list_price'])
        #print correctedprice
        inv.addToInventory(authors=titleinfo['authors'], categories=','.split(titleinfo['categories_as_string']), types=titleinfo['format'], isbn=titleinfo['isbn'], known_title=titleinfo['known_title'], listprice=correctedprice, ourprice=correctedprice, publisher=titleinfo['publisher'], title=titleinfo['title'], location_id=t.locationID, quantity=t.count, kind_name='books')



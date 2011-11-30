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
    try:
    	titleinfo=inv.lookup_by_isbn(t.isbn)
    except:
        #print "isbn %s seems to be invalid" % t.isbn
        pass
    #print titleinfo
    if isinstance(titleinfo['list_price'],unicode):
	correctedprice=float(titleinfo['list_price'].replace('$',''))
    else:
	correctedprice=float(titleinfo['list_price'])
    #print correctedprice
    inv.addToInventory(authors=titleinfo['authors'], categories=','.split(titleinfo['categories_as_string']), types=titleinfo['format'], isbn=titleinfo['isbn'], known_title=titleinfo['known_title'], price=correctedprice, publisher=titleinfo['publisher'], title=titleinfo['title'], location=t.location, quantity=t.count, kind_name='books')



import csv
from components.inventory import inventory
import etc

reader=csv.reader(open('/home/woodenshoe/Documents/inventory/inventory2009/film.csv'))
writer=csv.writer(open('/home/woodenshoe/Documents/inventory/inventory2009/faulty isbns.csv', 'w'))

inv=inventory()

for isbn, location, quantity in reader:
    item=0
    try:
        item=inv.lookup_by_isbn(isbn)
        #inv.addToInventory(publisher=item['publisher'], price=float(str(item['list_price']).lstrip('$')), title=item['title'], categories=item['categories_as_string'].split(","), authors=item['authors'], known_title=item['known_title'], owner=etc.default_owner, status='STOCK', kind_name='film', quantity=quantity, isbn=isbn, location=location)
    except Exception:
        print "in exception"
	print isbn, location, quantity
	writer.writerow((isbn, location, quantity))


